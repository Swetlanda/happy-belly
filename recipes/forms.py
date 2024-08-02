from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """
    Form to create a recipe by user
    """
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'instructions',
            'tags',
            'status',
            'image',  
            'image_alt',
            'serving',
        ]