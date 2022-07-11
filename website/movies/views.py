from django.shortcuts import render
from datetime import date



def film(request):
    context = {
        'title': "Film",

    }
    return render(request, 'movies/250.html', context)