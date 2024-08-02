from django.urls import path
from .views import (
    RecipeListView, 
    show_recipe, 
    create_recipe, 
    edit_recipe, 
    delete_recipe, 
    recipe_search, 
    welcome_page,
)


urlpatterns = [ 
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('view/<int:recipe_id>/', show_recipe, name='read'),
    path("create/", create_recipe, name="create"),
    path("edit/<int:recipe_id>", edit_recipe, name="edit"),
    path("delete/<int:recipe_id>", delete_recipe, name="delete"),
    path('search/', recipe_search, name='recipe_search'),
    path('welcome/', welcome_page, name='welcome'),  
]