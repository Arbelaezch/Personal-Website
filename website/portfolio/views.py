from django.shortcuts import render

def portfolio_base(request):
    context = {
    }
    return render(request, 'portfolio/portfolio_base.html', context)