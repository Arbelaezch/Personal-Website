from django.shortcuts import render
from datetime import date
from django.views.generic import DetailView
from .models import Project

def portfolio(request):
    context = {
        'year': date.today().year,
        'projects': Project.objects.all().order_by('-order'),
    }
    return render(request, 'portfolio/portfolio.html', context)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
