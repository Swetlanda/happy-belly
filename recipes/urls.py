from django.urls import path
from . import views


urlpatterns = [ 
    path("view/<recipe_id>", views.show_recipe, name="read"),
    path("", views.show_homepage, name="home"),
    path("create/", views.create_recipe, name="create"),
    path("edit/<recipe_id>", views.edit_recipe, name="edit"),
    path("delete/<recipe_id>", views.delete_recipe, name="delete"),

]