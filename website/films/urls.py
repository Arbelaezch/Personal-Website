from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('', views.top250_view, name='top_250'),
    path('<int:year>s/', views.decade_view, name='decade_view'),
    path('<int:year>s/<slug:slug>/', views.movie_detail_view, name='movie_detail'),
]