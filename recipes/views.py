from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import generic
from .models import Recipe
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class RecipeListView(generic.ListView):
    """
    Displays all recipes with pagination.
    """
    model = Recipe
    template_name = 'recipes/recipe_list.html'  
    context_object_name = 'recipes'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.filter(status=1)  

def homepage(request):
    """
    Displays the homepage. Redirects to welcome page if the user is logged in.
    """
    if request.user.is_authenticated:
        return redirect('welcome')
    return render(request, 'home.html')

@login_required
def welcome_page(request):
    """
    Displays a welcome page for logged-in users.
    """
    return render(request, 'recipes/welcome.html', {'user': request.user})

def show_recipe(request, recipe_id):
    """
    Displays a single recipe.
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    context = {
        "recipe": retrieved_recipe,
    }
    return render(request, 'recipes/view_recipe.html', context)

@login_required
def create_recipe(request):
    """
    Creates a new recipe for logged-in users.
    """
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your recipe was sussessfully created!")
            return redirect("home")
        else:
            messages.error(request, "There was an error in your form submission. Please try again.")
    else:
        form = RecipeForm()
        context = {"form": form, }
        return render(request, 'recipes/create_recipe.html', context)

@login_required
def edit_recipe(request, recipe_id):
    """
    Edits an existing recipe for logged-in users.
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    if not request.user == retrieved_recipe.user and not request.user.is_superuser:
        messages.error(request, "You cannot edit a recipe you did not create!")
        return redirect("home")

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=retrieved_recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Your recipe was updated!")
            return redirect("home")
        else:
            messages.error(request, "There was an error in your form submission. Please try again.")
        
    else:
        form = RecipeForm(instance=retrieved_recipe)
        context = {"form": form, "recipe": retrieved_recipe}
        return render(request, 'recipes/edit_recipe.html', context)

@login_required           
def delete_recipe(request, recipe_id):
    """
    Deletes an existing recipe for logged-in users.
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    if not request.user == retrieved_recipe.user and not request.user.is_superuser:
        messages.error(request, "You cannot delete a recipe you did not create!")
        return redirect("home")
    
    if request.method == "POST":
        retrieved_recipe.delete()
        messages.success(request, "Your recipe was deleted!")
        return redirect("home")
    else:
        context = {"recipe": retrieved_recipe,}
        return render(request, 'recipes/delete_recipe.html', context)

def recipe_search(request):
    """
    Search functionality for recipes.
    """
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.all()

    context = {
        'recipes': recipes,
        'query': query,
    }
    return render(request, 'recipes/recipe_list.html', context)