from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Recipe, Favorite


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = ('title', 'user', 'status', 'created_on', 'updated_on')
    search_fields = ['title', 'user__username', 'tags__name']
    list_filter = ('status', 'user', 'created_on', 'updated_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description', 'ingredients', 'instructions')


     # Ensure that pending recipes are also shown in the admin view
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Include recipes with both published (1) and pending (0) status
        return queryset.filter(status__in=[0, 1])


    def get_search_results(self, request, queryset, search_term):
        """
        Customises search in the admin to include results with tags.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            queryset |= self.model.objects.filter(
                tags__name__icontains=search_term
            )
        return queryset, use_distinct
        

class FavoriteAdmin(admin.ModelAdmin):
    """
    Manages display and filtering of the Favorite model in the admin interface.
    """
    list_display = ('user', 'recipe')
    search_fields = ['user__username', 'recipe__title']
    list_filter = ('user', 'recipe')
