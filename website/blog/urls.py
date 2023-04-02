from django.urls import path
from website import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.BlogView, name='BlogView'),
    path('blog/<int:article_id>', views.ArticleView, name='ArticleView'),
    # path('post/<int:post_id>', views.blogPost, name='blogPost'),
    # path('react/', views.react, name='react'),
    
]