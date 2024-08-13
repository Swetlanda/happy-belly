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
    my_recipes,
    my_favorites,
    add_to_favorites,
    remove_from_favorites,
)


urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('view/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path("create/", create_recipe, name="create_recipe"),
    path("preview/<int:recipe_id>/", recipe_preview, name='recipe_preview'),
    path("edit/<int:recipe_id>", edit_recipe, name="edit_recipe"),
    path("delete/<int:recipe_id>", delete_recipe, name="delete_recipe"),
    path('search/', recipe_search, name='recipe_search'),
    path('home/', homepage, name='home'),
    path('my_recipes/', my_recipes, name='my_recipes'),
    path('my_favorites/', my_favorites, name='my_favorites'),
    path(
        'add_to_favorites/<int:recipe_id>/',
        add_to_favorites,
        name='add_to_favorites'
    ),
    path(
        'remove_from_favorites/<int:recipe_id>/',
        remove_from_favorites,
        name='remove_from_favorites'
    ),
    path('welcome/', welcome_page, name='welcome'),
]
