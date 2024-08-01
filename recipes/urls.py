from django.urls import path
from . import views


urlpatterns = [ 
    path("view/<recipe_id>", views.show_recipe, name="read"),
    path('', views.recipe_list, name='recipe_list'),
    path("create/", views.create_recipe, name="create"),
    path("edit/<recipe_id>", views.edit_recipe, name="edit"),
    path("delete/<recipe_id>", views.delete_recipe, name="delete"),
    path('search/', views.recipe_search, name='recipe_search'),
    path('welcome/', views.welcome_page, name='welcome'),  
]