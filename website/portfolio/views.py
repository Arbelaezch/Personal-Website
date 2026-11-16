from django.shortcuts import render
from django.views.generic import DetailView
from .models import Project

def portfolio(request):
    context = {
        'projects': Project.objects.all().order_by('-order'),
    }
    return render(request, 'portfolio/portfolio.html', context)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} | Christian Arbelaez'
        context['page_description'] = self.object.subtitle
        return context
