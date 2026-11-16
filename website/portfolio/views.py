from django.db.models import F
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.conf import settings

from .models import PipelineItem, Project, Resume, SyncState

MORE_PROJECTS_ON_HOME = 6

HOME_DESCRIPTION = (
    'Christian Arbelaez is a full-stack developer who designs and maintains the pipelines '
    'that let AI agents ship software safely.'
)


def published_projects():
    # Newest GitHub activity first; projects without a repository follow in their hand-set order.
    return Project.objects.filter(is_published=True).order_by(F('github_pushed_at').desc(nulls_last=True), '-order')


PIPELINE_ROWS = 3


def pipeline_panel():
    """What the "How I ship with AI" panel shows, from the rows the GitHub sync stored.

    GitHub does not say which stage of the pipeline is running, so the panel only ever claims
    two things: a pull request is open ("working"), or nothing is ("idle").
    """
    items = list(PipelineItem.objects.all())
    merged = sorted((item for item in items if item.state == PipelineItem.MERGED),
                    key=lambda item: item.merged_at, reverse=True)
    for item in merged:
        item.result = 'Deployed' if item.repo in settings.DEPLOYING_REPOS else 'Merged'
    open_pulls = sorted((item for item in items if item.kind == PipelineItem.PULL and item.state == PipelineItem.OPEN),
                        key=lambda item: item.updated_at, reverse=True)
    queued = sorted((item for item in items if item.kind == PipelineItem.ISSUE),
                    key=lambda item: item.updated_at, reverse=True)
    return {
        'working_on': open_pulls[0] if open_pulls else None,
        'last_shipped': merged[0] if merged else None,
        'shipped': merged[:PIPELINE_ROWS],
        'queued': queued[:PIPELINE_ROWS],
        'synced_at': SyncState.last('pipeline'),
    }


def portfolio(request):
    featured = list(Project.objects.filter(is_published=True, is_featured=True).order_by('-order'))
    context = {
        'pipeline': pipeline_panel(),
        'featured': featured,
        'more_projects': published_projects().filter(is_featured=False)[:MORE_PROJECTS_ON_HOME],
        'page_description': HOME_DESCRIPTION,
    }
    return render(request, 'portfolio/portfolio.html', context)


def projects(request):
    context = {
        'projects': published_projects(),
        'page_title': 'Projects | Christian Arbelaez',
        'page_description': 'Everything Christian Arbelaez has built and published: web, mobile, AI tooling and games.',
    }
    return render(request, 'portfolio/projects.html', context)

class ProjectDetailView(DetailView):
    queryset = Project.objects.filter(is_published=True)
    template_name = 'portfolio/project_detail.html'

    # Case-study sections in reading order. A section with no content is left out of the page.
    SECTIONS = [
        ('problem', 'The problem'),
        ('description', 'What I built'),
        ('ai_usage', 'How AI was used'),
        ('safety', 'What kept it safe'),
        ('results', 'Results'),
        ('lessons_learned', 'Lessons and technologies'),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['page_title'] = f'{project.title} | Christian Arbelaez'
        context['page_description'] = project.display_summary
        context['sections'] = [
            {'heading': heading, 'html': getattr(project, field)}
            for field, heading in self.SECTIONS if getattr(project, field).strip()
        ]
        # Neighbours in the same order as the /projects/ page.
        others = list(published_projects().only('slug', 'title'))
        position = next((index for index, other in enumerate(others) if other.pk == project.pk), None)
        if position is not None:
            context['previous_project'] = others[position - 1] if position > 0 else None
            context['next_project'] = others[position + 1] if position + 1 < len(others) else None
        return context

def project_by_id(request, pk):
    # Project pages used to live at /project/<id>/; keep those links and search results working.
    project = get_object_or_404(Project, pk=pk, is_published=True)
    if not project.slug:
        project.save()  # save() builds the missing slug
    return redirect(project, permanent=True)

def resume(request):
    current = Resume.current()
    if current is None:
        raise Http404("No resume has been uploaded")
    try:
        pdf = current.file.open('rb')
    except FileNotFoundError:
        raise Http404("The resume file is missing")
    # Always the same download name, whatever the uploaded file was called.
    response = FileResponse(pdf, as_attachment=True, filename='Christian-Arbelaez-Resume.pdf', content_type='application/pdf')
    response['X-Robots-Tag'] = 'noindex'
    response['Cache-Control'] = 'no-cache'  # a new upload must reach visitors straight away
    return response
