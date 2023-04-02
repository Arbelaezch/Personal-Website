from django.urls import path
from website import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.blogHome, name='blog'),
    path('blog/<int:article_id>', views.blogArticle, name='blogArticle'),
    # path('post/<int:post_id>', views.blogPost, name='blogPost'),
    # path('react/', views.react, name='react'),
    
]