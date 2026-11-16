from django.contrib import admin
from .models import Project, Resume


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


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_current', 'file']
    list_editable = ['is_current']
    readonly_fields = ['uploaded_at']

    def delete_queryset(self, request, queryset):
        # The bulk "delete selected" action skips Model.delete(); go through it so the files are removed too.
        for resume in queryset:
            resume.delete()
