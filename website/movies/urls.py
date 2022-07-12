from django.urls import path
from website import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.film, name='film'),
    path('<str:decade>/', views.decade, name='decade'),
    path('<int:pk>/', views.movie, name='movie'),
]