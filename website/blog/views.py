from django.shortcuts import render
from datetime import date



def blog(request):
    context = {
        
    }
    return render(request, 'blog/blog.html', context)