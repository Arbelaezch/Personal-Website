from django.urls import path
from website import settings
from django.conf.urls.static import static
from .views import ProjectListView, ProjectDetailView

from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('', views.portfolio_base, name='portfolio_base'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]