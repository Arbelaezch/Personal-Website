from django.shortcuts import render



def index(request):
    context = {'latest_question_list': "test"}
    return render(request, 'polls/index.html', context)
