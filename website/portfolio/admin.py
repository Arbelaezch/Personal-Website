from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import path
from django.views.decorators.http import require_POST

from . import github
from .models import PipelineItem, Project, Resume, SyncState


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'is_featured', 'order', 'primary_language', 'github_repo']
    list_editable = ['is_published', 'is_featured', 'order']
    list_filter = ['is_published', 'is_featured', 'primary_language']
    search_fields = ['title', 'subtitle', 'summary', 'github_repo']
    prepopulated_fields = {'slug': ['title']}
    # Written by the GitHub sync, never by hand.
    readonly_fields = ['github_description', 'github_pushed_at']
    change_list_template = 'admin/portfolio/project/change_list.html'

    def get_urls(self):
        sync = self.admin_site.admin_view(require_POST(self.sync_view))
        return [path('sync-github/', sync, name='portfolio_project_sync_github')] + super().get_urls()

    def sync_view(self, request):
        """The "Sync from GitHub now" button: the same work as the daily timer."""
        if not self.has_change_permission(request):
            raise PermissionDenied
        lines = []
        succeeded = [github.sync_projects(lines.append), github.sync_pipeline(lines.append)]
        level = messages.SUCCESS if all(succeeded) else messages.ERROR
        for line in lines:
            self.message_user(request, line, level if 'FAILED' in line or all(succeeded) else messages.INFO)
        return redirect('admin:portfolio_project_changelist')

    def changelist_view(self, request, extra_context=None):
        extra_context = {**(extra_context or {}), 'last_github_sync': SyncState.last('projects')}
        return super().changelist_view(request, extra_context)
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


@admin.register(PipelineItem)
class PipelineItemAdmin(admin.ModelAdmin):
    """Read-only: the GitHub sync rewrites these rows on every run."""
    list_display = ['repo', 'number', 'kind', 'state', 'title', 'merged_at']
    list_filter = ['repo', 'kind', 'state']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
