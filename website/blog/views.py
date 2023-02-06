from django.shortcuts import render
from datetime import date



def blogHome(request):
    context = {
        "year": date.today().year,
    }
    return render(request, 'blog/blog.html', context)


def react(request):
    context = {
        "year": date.today().year,
    }
    return render(request, 'blog/react.html', context)
