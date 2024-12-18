from django.urls import path
from . import views
# from recipes.views import 

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
]
