from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            return redirect('register')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes')
    else:
        form = LoginForm()
    return render(request, 'RecipeApp/home.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            profile_picture = form.cleaned_data.get('profile_picture')

            user = User.objects.create_user(username=username, email=email, password=password)

            if profile_picture:
                user.profile_picture = profile_picture

            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    else:
        form = RegistrationForm()
    return render(request, 'RecipeApp/registration.html', {'form': form})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            recipe = form.save(commit=False)
            recipe.user = user  # Assign the user to the recipe
            recipe.save()
            return redirect('recipes')
    else:
        form = RecipeForm()
    return render(request, 'RecipeApp/create_recipe.html', {'form': form})


def recipe_list(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    else:
        form = RecipeForm()

    recipes = Recipe.objects.all().order_by('-id')

    return render(request, 'RecipeApp/recipe_list.html', {'recipes': recipes, 'form': form})


def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'RecipeApp/recipe_details.html', {'recipe': recipe})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required  # Requires the user to be logged in to access this view
def delete_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)

        # Check if the authenticated user is the owner of the recipe
        if recipe.user == request.user:
            recipe.delete()
            # Redirect to the recipe list page after deleting
            return redirect('recipes')
        else:
            # Handle unauthorized access (user didn't create the recipe)
            return render(request, 'RecipeApp/403.html', status=403)
    except Recipe.DoesNotExist:
        # Handle the case where the recipe doesn't exist
        return render(request, 'RecipeApp/404.html', status=404)
