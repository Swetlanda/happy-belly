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
    preview = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance