from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


STATUS_CHOICES = [
        (0, "Draft"),
        (1, "Published")
]
# Defines choices for the status field of the recipe - draft or published.

SERVING_CHOICES = [
        (2, '2 people'),
        (4, '4 people'),
        (6, '6 people'),
        (8, '8 people'),
]
# Defines choices for the serving field of the recipe - 2, 4, 6 or 8 servings.


# Custom-made model Favorite
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey('Recipe', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'recipe')
    # Ensures that a user can only favorite a recipe once.

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'
    # Returns a string representation of the Favorite object.


# Custom-made model Recipe
class Recipe(models.Model):
    title = models.CharField(max_length=150, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    tags = TaggableManager()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    image = CloudinaryField('image', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True, null=True)
    serving = models.IntegerField(choices=SERVING_CHOICES, default=4)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    # Orders the recipes by creation date, with the most recent first.

    def __str__(self):
        return f'"{self.title}" by {self.user}'
    # Returns a string representation of the Recipe object.

    def generate_unique_slug(self):
        """
        Generates a unique slug for the recipe.
        If the generated slug already exists,
        appends a unique suffix to make it unique.
        """
        original_slug = slugify(self.title)
        queryset = Recipe.objects.filter(slug__iexact=original_slug).exists()
        slug = original_slug
        unique_suffix = 1
        while queryset:
            slug = f"{original_slug}-{unique_suffix}"
            queryset = Recipe.objects.filter(slug__iexact=slug).exists()
            unique_suffix += 1
        return slug


@receiver(pre_save, sender=Recipe)
def populate_slug(sender, instance, **kwargs):
    """
    This function automatically generates a unique slug from the recipe title
    using the generate_unique_slug method.
    """
    if not instance.slug:
        instance.slug = slugify(instance.title)
