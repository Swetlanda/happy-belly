from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """
    Form to create a new recipe by logged-in user.
    Inherits from Django's ModelForm, automatically generating form fields
    based on the Recipe model.
    """
    class Meta:
        model = Recipe
        # Exclude the "status" field and set a custom label "image description"
        exclude = ['status']
        # Provide a user-friendly label for the image_alt field
        labels = {
            'image_alt': 'Image description'
        }
        # Define the fields to be included in the form
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
        # Customise the widgets for each field to apply CSS classes for styling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}
            ),
            'image_alt': forms.TextInput(attrs={'class': 'form-control'}),
            'serving': forms.Select(attrs={'class': 'form-control'}),
        }

    # Hidden field to manage form previews; defaults to False.
    preview = forms.BooleanField(
        widget=forms.HiddenInput, required=False, initial=False
    )

    def save(self, commit=True):
        """
        Custom save method for saving process to allow Preview of recipe.
        - If commit is True, the instance is saved to the database
        and many-to-many relationships (tags) are updated.
        - If commit is False, the instance is returned
        but not saved to the database.
        """
        # Save the form data without committing to the database
        instance = super().save(commit=False)
        if commit:
            instance.save()  # Save the instance to the database
            self.save_m2m()  # Save many-to-many relationships (tags)
        return instance  # Return the saved instance
