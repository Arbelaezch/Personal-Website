from django.shortcuts import render


def portfolio(request):
    
    context = {
        'title': 'Portfolio',
        
    }
    return render(request, 'portfolio/portfolio.html', context)