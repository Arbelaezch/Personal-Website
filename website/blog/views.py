from django.shortcuts import render
from datetime import date
from .models import Article



def BlogView(request):

    context = {
        "articles": Article.objects.all(),
    }

    return render(request, 'blog/blog.html', context)


def ArticleView(request, article_id):

    context = {

    }

    return render(request, 'blog/article.html', context)
