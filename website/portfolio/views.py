from django.shortcuts import render
from datetime import date



def portfolio(request):
    context = {
        'year': date.today().year,
    }
    return render(request, 'portfolio/portfolio.html', context)

def portfolio_base(request):
    context = {
    }
    return render(request, 'portfolio/portfolio_base.html', context)