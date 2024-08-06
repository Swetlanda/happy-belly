from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """
    Form to create a recipe by user
    """
    class Meta:
        model = Recipe
        # Exclude the "status" field and set a custom label for "image_alt" - "image description" to simplify language for users
        exclude = ['status']
        labels = {
            'image_alt': 'Image description'
        }
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
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image_alt': forms.TextInput(attrs={'class': 'form-control'}),
            'serving': forms.Select(attrs={'class': 'form-control'}),
        }
    preview = forms.BooleanField(widget=forms.HiddenInput, required=False, initial=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance