from django.urls import path

from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('personal/', views.personal, name='personal'),
    # Listed first: an all-digit path is an old id link, never a slug (slugs are not digits only).
    path('project/<int:pk>/', views.project_by_id, name='project_by_id'),
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
