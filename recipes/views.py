from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import generic
from .models import Recipe, Favorite
from .forms import RecipeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.html import strip_tags


class RecipeListView(generic.ListView):
    """
    Displays a list of all recipes with a published status (status=1)
    with pagination of 8 recipes per page.
    Accessible for all visitors (no log-in required to view recipes).
    """
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.filter(status=1)


def homepage(request):
    """
    Displays the homepage for all visitors.
    Redirects to welcome page if the user is logged in.
    """
    if request.user.is_authenticated:
        return redirect('welcome')

    all_recipes = Recipe.objects.filter(status=1)
    context = {
        'recipes': all_recipes,
    }
    return render(request, 'home.html', context)


@login_required
def welcome_page(request):
    """
    Displays a welcome page for logged-in users.
    Shows the user's own recipes - My Recipes.
    Shows the user's favorites recipes - My Favorites.
    """
    user_recipes = Recipe.objects.filter(user=request.user, status=1)
    context = {
        'user': request.user,
        'recipes': user_recipes,
    }
    return render(request, 'recipes/welcome.html', context)


def view_recipe(request, recipe_id):
    """
    Displays a single full recipe for all visitors.
    If the user is logged-in, manages favorite status
    by adding/removing favourite recipe.
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    # Checks if the user has added the recipe to favorites.
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, recipe=retrieved_recipe).exists()

    # Manages favorites - add/remove favourite recipe.
    if request.method == "POST":
        if request.user.is_authenticated:
            if 'add_to_favorites' in request.POST:
                return add_to_favorites(request, recipe_id)
            elif 'remove_from_favorites' in request.POST:
                return remove_from_favorites(request, recipe_id)
        else:
            messages.error(
                request,
                "You need to be logged in to add recipes to favorites."
            )
            return redirect('account_login')

    context = {
        "recipe": retrieved_recipe,
        "is_favorite": is_favorite,
    }
    return render(request, 'recipes/view_recipe.html', context)


@login_required
def create_recipe(request):
    """
    Allows logged-in users to create a new recipe.
    The recipe is saved with a pending status (subject to admin's approval).
    Preview data is stored in the session to allow Preview recipe page later.
    """
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.status = 0   # Pending admin's approval
            new_recipe.save()
            form.save_m2m()   # Tags - save many-to-many relationships

            # Store preview data in the session to be used for Preview recipe
            store_preview_data_in_session(request, new_recipe)

            messages.success(request, "This is a preview of your recipe.")
            return redirect('recipe_preview', recipe_id=new_recipe.id)
        else:
            messages.error(
                request,
                "There was an error in your form submission. Please try again."
            )
    else:
        form = RecipeForm()

    context = {
        'form': form
    }
    return render(request, 'recipes/create_recipe.html', context)


@login_required
def store_preview_data_in_session(request, recipe):
    """
    Stores recipe data in the session for preview purposes.
    This is used to pass data to the recipe Preview page.
    """
    # Clear any existing preview data to avoid conflicts
    request.session.pop('preview_data', None)
    request.session.pop('preview_image', None)

    # Store the latest data
    request.session['preview_data'] = {
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'tags': ', '.join([tag.name for tag in recipe.tags.all()]),
        'serving': recipe.get_serving_display(),
        'image_url': recipe.image.url if recipe.image else None,
        'image_alt': recipe.image_alt,
    }

    if recipe.image:
        request.session['preview_image'] = recipe.image.url


@login_required
def recipe_preview(request, recipe_id):
    """
    Dispays a previw of the recipe before submission for logged-in users.
    The user can either select Submit for approval or Edit again.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    preview_data = request.session.get('preview_data', None)

    if request.method == "POST":
        # If Confirm, save recipe and send to admin for approval
        if 'confirm' in request.POST:  # Submit for approval
            # Assign the data from the Preview to the recipe object
            if preview_data:
                recipe.title = preview_data['title']
                recipe.description = preview_data['description']
                recipe.ingredients = preview_data['ingredients']
                recipe.instructions = preview_data['instructions']
                recipe.image_alt = preview_data['image_alt']

            recipe.status = 0  # Set status to pending for admin's approval
            recipe.save()  # Save the recipe to the database
            messages.success(
                request,
                "Your recipe has been sent to the admin for approval."
            )
            return redirect('recipe_list')
        # If Edit, redirect to Edit recipe again
        elif 'edit' in request.POST:
            messages.info(request, "You can continue to edit the recipe.")
            return redirect('edit_recipe', recipe_id=recipe.id)

    context = {
        'preview_data': preview_data,
        'recipe': recipe   # Pass the recipe to ensure it’s used correctly
    }
    return render(request, 'recipes/recipe_preview.html', context)


@login_required
def edit_recipe(request, recipe_id):
    """
    Allows logged-in users to edit an existing recipe
    (if the user created this recipe earlier).
    The user can preview the recipe or submit the changes for admin's approval.
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    # Ensure that the user has created this recipe earlier or a superuser
    if (
        not request.user == retrieved_recipe.user
        and not request.user.is_superuser
    ):
        messages.error(request, "You cannot edit a recipe you did not create!")
        return redirect("home")

    if request.method == "POST":
        form = RecipeForm(
            request.POST, request.FILES, instance=retrieved_recipe
        )
        if form.is_valid():
            updated_recipe = form.save(commit=False)

            # If press Submit, save recipe and send to admin for approval
            # Submit changes for approval
            if 'submit' in request.POST:
                # Set status to pending for admin's approval
                updated_recipe.status = 0
                updated_recipe.save()
                # Tags - save many-to-many relationships
                form.save_m2m()
                messages.success(
                    request,
                    "Your changes have been submitted for approval."
                )
                return redirect('recipe_list')

            # If press Preview, redirect to Recipe preview.
            elif 'preview' in request.POST:   # Preview changes
                store_preview_data_in_session(request, updated_recipe)
                return redirect(
                    'recipe_preview', recipe_id=retrieved_recipe.id
                )

        else:
            messages.error(
                request,
                "There was an error in your form submission. Please try again."
            )

    else:
        # Convert HTML content to plain text before loading into the form
        ingredients_text = strip_tags(
            retrieved_recipe.ingredients
        ).replace('&nbsp;', '').replace('\n', '')
        instructions_text = strip_tags(
            retrieved_recipe.instructions
        ).replace('&nbsp;', '').replace('\n', '')

        # Initialise the form with current recipe data
        form = RecipeForm(instance=retrieved_recipe, initial={
            'ingredients': ingredients_text,
            'instructions': instructions_text
        })

        # Set the initial value for tags
        form.initial['tags'] = ', '.join(
            [tag.name for tag in retrieved_recipe.tags.all()]
        )

    context = {
        'form': form,
        'recipe': retrieved_recipe
    }
    return render(request, 'recipes/edit_recipe.html', context)


@login_required
def delete_recipe(request, recipe_id):
    """
    Allows logged-in users to delete an existing recipe
    (if the recipe has been created earlier by this user).
    """
    retrieved_recipe = get_object_or_404(Recipe, id=recipe_id)

    if (
        not request.user == retrieved_recipe.user
        and not request.user.is_superuser
    ):
        messages.error(
            request,
            "You cannot delete a recipe you did not create!"
        )
        return redirect("home")

    if request.method == "POST":
        retrieved_recipe.delete()
        messages.success(request, "Your recipe was deleted!")
        return redirect("home")

    else:
        context = {
            "recipe": retrieved_recipe,
        }
        return render(request, 'recipes/delete_recipe.html', context)


def recipe_search(request):
    """
    Search functionality for recipes including title, description, ingredients,
    instructions, and tags. Available for all users.
    """
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(instructions__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
        'query': query,
    }
    return render(request, 'recipes/recipe_search.html', context)


@login_required
def my_recipes(request):
    """
    Displays all recipes created by the current user (only published).
    Availabe for logged-in users.
    """
    user_recipes = Recipe.objects.filter(
        user=request.user, status=1
    )
    context = {
        'recipes': user_recipes,
    }
    return render(request, 'recipes/my_recipes.html', context)


@login_required
def my_favorites(request):
    """
    Displays all recipes that the current user has added to favorites.
    Availabe for logged-in users.
    """
    favorite_recipes = Favorite.objects.filter(
        user=request.user).select_related('recipe')
    context = {
        'favorites': favorite_recipes,
    }
    return render(request, 'recipes/my_favorites.html', context)


@login_required
def add_to_favorites(request, recipe_id):
    """
    Adds a recipe to the user's favorites.
    If the recipe is already in favorites, an appropriate message is displayed.
    Availabe for logged-in users.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user, recipe=recipe)

    if created:
        messages.success(request, "Recipe added to your favorites.")

    else:
        messages.info(request, "Recipe is already in your favorites.")

    return redirect('view_recipe', recipe_id=recipe.id)


@login_required
def remove_from_favorites(request, recipe_id):
    """
    Removes a recipe from the user's favorites.
    Availabe for logged-in users.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        Favorite.objects.filter(user=request.user, recipe=recipe).delete()
        messages.success(request, "Recipe removed from your favorites.")

    return redirect('my_favorites')
