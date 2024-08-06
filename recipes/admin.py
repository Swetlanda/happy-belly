from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'user', 'status', 'created_on')
    search_fields = ['title', 'user__username', 'tags__name']  
    list_filter = ('status', 'created_on', 'user')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('description', 'ingredients', 'instructions')

    def save_model(self, request, obj, form, change):
        if obj.status == 1 and not obj.pk:
            obj.status = 0  
        super().save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            queryset |= self.model.objects.filter(tags__name__icontains=search_term)

        return queryset, use_distinct

