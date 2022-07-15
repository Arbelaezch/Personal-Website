from django.shortcuts import render


def food(request):
    context = {
    }
    return render(request, 'food/food.html', context)