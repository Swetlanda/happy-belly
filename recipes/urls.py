from django.urls import path
from .views import (
    RecipeListView, 
    view_recipe, 
    create_recipe, 
    recipe_preview,
    edit_recipe, 
    delete_recipe, 
    recipe_search, 
    welcome_page,
    homepage,
)


urlpatterns = [ 
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('view/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path("create/", create_recipe, name="create_recipe"),
    path("preview/<int:recipe_id>/", recipe_preview, name='recipe_preview'),  
    path("edit/<int:recipe_id>", edit_recipe, name="edit_recipe"),
    path("delete/<int:recipe_id>", delete_recipe, name="delete_recipe"),
    path('search/', recipe_search, name='recipe_search'),
    path('welcome/', welcome_page, name='welcome'),  
]