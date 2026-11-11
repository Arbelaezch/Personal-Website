from django.urls import path

from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]
