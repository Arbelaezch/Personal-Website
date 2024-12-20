from django.shortcuts import render
from datetime import date
# import pyrebase
import os
from django.views.generic import ListView, DetailView
from .models import Project

def portfolio(request):
    context = {
        'year': date.today().year,
        'projects': Project.objects.all().order_by('-order'),
    }
    return render(request, 'portfolio/portfolio.html', context)

def portfolio_base(request):
    context = {
    }
    return render(request, 'portfolio/portfolio_base.html', context)

class ProjectListView(ListView):
    # * Unused
    model = Project
    context_object_name = 'projects'
    template_name = 'portfolio/templates/portfolio/portfolio.html'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
