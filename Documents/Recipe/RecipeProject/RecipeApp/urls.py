from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', views.user_login, name='home'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('recipes/', views.recipe_list, name='recipes'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('recipes/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)