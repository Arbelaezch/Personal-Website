from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'is_featured', 'order', 'primary_language', 'github_repo']
    list_editable = ['is_published', 'is_featured', 'order']
    list_filter = ['is_published', 'is_featured', 'primary_language']
    search_fields = ['title', 'subtitle', 'summary', 'github_repo']
    prepopulated_fields = {'slug': ['title']}
    # Written by the GitHub sync, never by hand.
    readonly_fields = ['github_description', 'github_pushed_at']
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'subtitle', 'summary', 'category', 'primary_language', 'timeline']}),
        ('Visibility', {'fields': ['is_published', 'is_featured', 'order']}),
        ('Content', {'fields': ['image', 'description', 'lessons_learned']}),
        ('Links', {'fields': ['project_url', 'github_url']}),
        ('GitHub sync', {'fields': ['github_repo', 'github_description', 'github_pushed_at']}),
    ]
