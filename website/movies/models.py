from django.db import models
from django import forms

DECADE_LIST = [
    ('1900s', '1900'),
    ('1930s', '1930'),
    ('1940s', '1940'),
    ('1950s', '1950'),
    ('1960s', '1960'),
    ('1970s', '1970'),
    ('1980s', '1980'),
    ('1990s', '1990'),
    ('2000s', '2000'),
    ('2010s', '2010'),
    ('2020s', '2020'),
]


class Film(models.Model):
    title = models.CharField(max_length=200)
    year = models.DateTimeField('date published')
    director = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class Decade(models.Model):
    decade = models.CharField(max_length=50, choices=DECADE_LIST)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.title