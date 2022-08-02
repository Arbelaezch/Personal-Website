from django.urls import path
from website import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.portfolio_base, name='portfolio_base'),
]