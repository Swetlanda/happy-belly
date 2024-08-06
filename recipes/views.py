from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import generic
from .models import Recipe, Favorite
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import upload
from django.db.models import Count


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

def view_recipe(request, recipe_id):
    """
    Displays a single recipe and allows for adding/removing from favorites (for logged-in users).
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the user has added the recipe to favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=retrieved_recipe).exists()

    # Add/remove favorites
    if request.method == "POST":
        if request.user.is_authenticated:
            if 'add_to_favorites' in request.POST:
                return add_to_favorites(request, recipe_id)
            elif 'remove_from_favorites' in request.POST:
                return remove_from_favorites(request, recipe_id)
        else:
            messages.error(request, "You need to be logged in to add recipes to favorites.")
            return redirect('account_login')

    context = {
        "recipe": retrieved_recipe,
        "is_favorite": is_favorite,
    }

    return render(request, 'recipes/view_recipe.html', context)

@login_required
def create_recipe(request):
    """
    Creates a new recipe for logged-in users.
    """
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.status = 0  
            new_recipe.save()
            form.save_m2m()  

            # Store preview data in the session without attempting to access the image URL
            request.session['preview_data'] = {
                'title': new_recipe.title,
                'description': new_recipe.description,
                'ingredients': new_recipe.ingredients,
                'instructions': new_recipe.instructions,
                'image_url': new_recipe.image.url if new_recipe.image else None,
                'tags': [tag.name for tag in new_recipe.tags.all()],
                'serving': new_recipe.get_serving_display(),
                'image_alt': new_recipe.image_alt,
            }

            # Handle image preview separately if needed
            if new_recipe.image:
                request.session['preview_image'] = new_recipe.image.url

            messages.success(request, "This is a preview of your recipe.")
            return redirect('recipe_preview', recipe_id=new_recipe.id)
        else:
            messages.error(request, "There was an error in your form submission. Please try again.")
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/create_recipe.html', {'form': form})

@login_required
def recipe_preview(request, recipe_id):
    """
    Previews a recipe before submission - user can select Susbmit for approval or Edit again.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    preview_data = request.session.get('preview_data', None)
      
    if request.method == "POST":
        # If POST request, change status for pending approval or or redirect to edit page again 
        if 'confirm' in request.POST:  
            recipe.status = 0  
            recipe.save()
            messages.success(request, "Your recipe has been sent to the admin for approval.")
            return redirect('recipe_list')
        elif 'edit' in request.POST:  
            messages.info(request, "Continuing to edit the recipe.")
            return redirect('edit_recipe', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_preview.html', {'preview_data': preview_data})

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
        if 'submit' in request.POST:
            form = RecipeForm(request.POST, request.FILES, instance=retrieved_recipe)
            if form.is_valid():
                updated_recipe = form.save(commit=False)
                updated_recipe.status = 0  
                updated_recipe.save()
                form.save_m2m()

                messages.success(request, "Your changes have been submitted for approval.")
                return redirect('recipe_list')
            else:
                messages.error(request, "There was an error in your form submission. Please try again.")
        elif 'preview' in request.POST:
            form = RecipeForm(request.POST, request.FILES, instance=retrieved_recipe)
            if form.is_valid():
                updated_recipe = form.save(commit=False)

                # Store form data in session for preview
                request.session['preview_data'] = {
                    'title': updated_recipe.title,
                    'description': updated_recipe.description,
                    'ingredients': updated_recipe.ingredients,
                    'instructions': updated_recipe.instructions,
                    'image_url': updated_recipe.image.url if updated_recipe.image else None,
                    'tags': [tag.name for tag in updated_recipe.tags.all()],
                    'serving': updated_recipe.get_serving_display(),
                    'image_alt': updated_recipe.image_alt,
                }
                return redirect('recipe_preview', recipe_id=retrieved_recipe.id)
    else:
        form = RecipeForm(instance=retrieved_recipe)
    
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': retrieved_recipe})


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

@login_required
def my_recipes(request):
    """
    Display all recipes created by the current user.
    """
    user_recipes = Recipe.objects.filter(user=request.user, status=1)
    return render(request, 'recipes/my_recipes.html', {'recipes': user_recipes})

@login_required
def my_favorites(request):
    """
    Display all recipes that the current user has added to favorites.
    """
    favorite_recipes = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/my_favorites.html', {'favorites': favorite_recipes})

@login_required
def add_to_favorites(request, recipe_id):
    """
    Add a recipe to the user's favorites.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if created:
        messages.success(request, "Recipe added to your favorites.")
    else:
        messages.info(request, "Recipe is already in your favorites.")
    return redirect('view_recipe', recipe_id=recipe.id)

@login_required
def remove_from_favorites(request, recipe_id):
    """
    Remove a recipe from the user's favorites.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    messages.success(request, "Recipe removed from your favorites.")
    return redirect('view_recipe', recipe_id=recipe.id)
