from django.shortcuts import render
from datetime import date
# import pyrebase
import os

# config = {
#     'apiKey': "AIzaSyCu5NlrJfwVDrx8XJdMyQ6oG4aEDYE-YOk",
#     'authDomain': "personal-website-476d1.firebaseapp.com",
#     "databaseURL": 'gs://personal-website-476d1.appspot.com',
#     'projectId': "personal-website-476d1",
#     'storageBucket': "personal-website-476d1.appspot.com",
#     'messagingSenderId': "58045340082",
#     'appId': "1:58045340082:web:4f97b773bc830bf635acab"
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()


def portfolio(request):
    context = {
        'year': date.today().year,
    }
    return render(request, 'portfolio/portfolio.html', context)

def portfolio_base(request):
    context = {
    }
    return render(request, 'portfolio/portfolio_base.html', context)
