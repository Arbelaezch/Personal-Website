from django.shortcuts import render
from datetime import date



def film(request):
    context = {
        'title': "Film",

    }
    return render(request, 'movies/250.html', context)


def decade(request):
    context = {
        'title': "Decade",
    }
    return render(request, 'movies/decade.html', context)

def movie(request):
    context = {
        'title': "Film",
    }
    return render(request, 'movies/film.html', context)