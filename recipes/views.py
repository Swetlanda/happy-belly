from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views import generic
from .models import Recipe
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import upload


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
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.status = 0  # Set status to draft
            new_recipe.save()
            form.save_m2m()  # Save the many-to-many data for tags

            request.session['preview_data'] = {
                'title': new_recipe.title,
                'description': new_recipe.description,
                'ingredients': new_recipe.ingredients,
                'instructions': new_recipe.instructions,
                'image_url': new_recipe.image.url if new_recipe.image else None,
                'tags': [tag.name for tag in new_recipe.tags.all()],
                'serving': new_recipe.get_serving_display(),
            }
            messages.success(request, "Your recipe has been created. Do you want to preview your recipe?")
            return redirect('recipe_preview', recipe_id=new_recipe.id)
        else:
            messages.error(request, "There was an error in your form submission. Please try again.")
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/create_recipe.html', {'form': form})

@login_required
def recipe_preview(request, recipe_id):
    """
    Previews a recipe before submission.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    preview_data = request.session.get('preview_data', None)

    if preview_data:
        preview_data = {
            'title': preview_data.get('title', recipe.title),
            'description': preview_data.get('description', recipe.description),
            'ingredients': preview_data.get('ingredients', recipe.ingredients),
            'instructions': preview_data.get('instructions', recipe.instructions),
            'image_url': preview_data.get('image_url', recipe.image.url if recipe.image else None),
            'tags': preview_data.get('tags', [tag.name for tag in recipe.tags.all()]),
            'serving': preview_data.get('serving', recipe.get_serving_display()),
        }
    else:
        preview_data = {
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'image_url': recipe.image.url if recipe.image else None,
            'tags': [tag.name for tag in recipe.tags.all()],
            'serving': recipe.get_serving_display(),
        }
    
    if request.method == "POST":
        if 'confirm' in request.POST:  # Check for confirm button
            # Set recipe status to pending approval
            recipe.status = 0  # Or any status that means "pending approval"
            recipe.save()
            messages.success(request, "Your recipe has been sent to the admin for approval.")
            return redirect('recipe_list')
        elif 'edit' in request.POST:  # Check for edit button
            messages.info(request, "Continuing to edit the recipe.")
            return redirect('edit_recipe', recipe_id=recipe.id)

    return render(request, 'recipes/preview_recipe.html', {'preview_data': preview_data})

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
            updated_recipe = form.save(commit=False)
            updated_recipe.status = 0  
            updated_recipe.save()
            form.save_m2m() 

            request.session['preview_data'] = {
                'title': updated_recipe.title,
                'description': updated_recipe.description,
                'ingredients': updated_recipe.ingredients,
                'instructions': updated_recipe.instructions,
                'image_url': updated_recipe.image.url if updated_recipe.image else None,
                'tags': [tag.name for tag in updated_recipe.tags.all()],
                'serving': updated_recipe.get_serving_display(),
            }

            messages.success(request, "Your changes have been saved. Do you want to preview the recipe?")
            return redirect('recipe_preview', recipe_id=retrieved_recipe.id)
        else:
            messages.error(request, "There was an error in your form submission. Please try again.")
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