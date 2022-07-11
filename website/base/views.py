from django.shortcuts import render
from datetime import date



def index(request):
    context = {
        'title': "Welcome!",
        'year': date.today().year,
    }
    return render(request, 'base/index.html', context)

