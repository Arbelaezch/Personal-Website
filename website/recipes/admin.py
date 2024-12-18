from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('is_published',)
    fieldsets = (
        ('Required', {
            'fields': ('title', 'ingredients', 'directions')
        }),
        ('Optional', {
            'fields': (
                'rating', 'slug', 'description', 'servings', 'prep_time', 
                'cook_time', 'difficulty', 'category', 'image', 'created_at', 
                'updated_at')
        }),
    )

