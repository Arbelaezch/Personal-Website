from django.shortcuts import render
from .models import Article



def BlogView(request):

    context = {
        "articles": Article.get_reverse_chronological_order(),
        "page_title": "Blog | Christian Arbelaez",
    }

    return render(request, 'blog/blog.html', context)


def ArticleView(request, article_id):

    context = {

    }

    return render(request, 'blog/article.html', context)
