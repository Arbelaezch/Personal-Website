from django.db.models import F
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from .models import Project, Resume

MORE_PROJECTS_ON_HOME = 6

HOME_DESCRIPTION = (
    'Christian Arbelaez is a full-stack developer who designs and maintains the pipelines '
    'that let AI agents ship software safely.'
)


def published_projects():
    # Newest GitHub activity first; projects without a repository follow in their hand-set order.
    return Project.objects.filter(is_published=True).order_by(F('github_pushed_at').desc(nulls_last=True), '-order')


def portfolio(request):
    featured = list(Project.objects.filter(is_published=True, is_featured=True).order_by('-order'))
    context = {
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} | Christian Arbelaez'
        context['page_description'] = self.object.display_summary
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
