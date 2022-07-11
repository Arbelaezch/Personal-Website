from django.urls import path

from . import views

urlpatterns = [
    path('', views.film, name='film'),
    path('decade/', views.decade, name='decade'),
    path('movie/', views.movie, name='movie'),
]