from django.shortcuts import render
from datetime import date
import csv
import pandas as pd
import os

from movies.models import Decade, Film
# from movies import top250


def film(request):
    favorites_list = []
    csvfile = os.path.join(os.path.dirname(__file__), 'test.csv')
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                movie = Film.objects.filter(title=row[0]).first()

                favorites_list.append({'title': movie.title, 'year': movie.year, 'decade': movie.decade_fk, 'pk': movie.pk},)
                line_count += 1

    # csvfile = request.FILES['top250']
    # data = pd.read_csv(csvfile)
    #You can create your custom dataframe here before converting it to html in next line
    # data_html = data.to_html() 
    # context = {'loaded_data': data_html}
    # return render(request, "dataflow/table.html", context)

    decades = Decade.objects.all()
    context = {
        'title': "Film",
        'decades': decades,
        'favorites_list': favorites_list,
    }
    return render(request, 'movies/250.html', context)

def decade(request, decade):
    decade_obj = Decade.objects.filter(decade=decade).first()

    # Gets all films from the selected decade, cuz fk's are weird.
    films = Film.objects.filter(decade_fk__decade=decade_obj.decade)

    context = {
        'title': f"{decade}s",
        'decade_obj': decade_obj,
        'movie_list': films,
    }
    return render(request, 'movies/decade.html', context)

def movie(request, decade, pk):
    film = Film.objects.get(pk=pk)
    print(film.image.url)

    context = {
        'title': film.decade_fk,
        'film': film,

    }
    return render(request, 'movies/film.html', context)