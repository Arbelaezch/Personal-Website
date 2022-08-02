from django.shortcuts import render

def portfolio(request):
    context = {
    }
    return render(request, 'portfolio/portfolio.html', context)

def portfolio_base(request):
    context = {
    }
    return render(request, 'portfolio/portfolio_base.html', context)