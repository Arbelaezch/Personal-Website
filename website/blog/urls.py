from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogView, name='BlogView'),
    path('blog/<int:article_id>', views.ArticleView, name='ArticleView'),
]