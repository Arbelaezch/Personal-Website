from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from .models import Project

def portfolio(request):
    context = {
        'projects': Project.objects.filter(is_published=True).order_by('-order'),
    }
    return render(request, 'portfolio/portfolio.html', context)

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
