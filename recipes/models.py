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

SERVING_CHOICES = [
        (2, '2 people'),
        (4, '4 people'),
        (6, '6 people'),
        (8, '8 people'),
]


# Create your models here.
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
        ordering = ["created_on"]

    def __str__(self):
        return f'"{self.title}" by {self.user}'

# A function to automatically generate a slug from the title before saving the model instance.
@receiver(pre_save, sender=Recipe)
def populate_slug(sender, instance, **kwargs):
    """
    This function automatically generates a slug from the recipe title using the slugify function if the slug field is empty. 
    """
    if not instance.slug:
        instance.slug = slugify(instance.title)

    

    


