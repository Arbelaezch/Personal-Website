from django.shortcuts import render
from datetime import date

from movies.models import Decade, Film



def film(request):
    decades = Decade.objects.all()
    context = {
        'title': "Film",
        'decades': decades,
        
    }
    return render(request, 'movies/250.html', context)


def decade(request, decade):
    decade_obj = Decade.objects.filter(decade=decade).first()

    # Gets all films from the selected decade, cuz fk's are weird.
    films = Film.objects.filter(decade_fk__decade=decade_obj.decade)

    context = {
        'title': f"{decade}s",
        'decade_obj': decade_obj,
        'movie_list': Film.objects.filter(decade_fk__decade=decade_obj.decade),
    }
    return render(request, 'movies/decade.html', context)

def movie(request):
    context = {
        'title': "Film",
    }
    return render(request, 'movies/film.html', context)