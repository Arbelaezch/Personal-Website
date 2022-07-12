from re import T
from django.db import models
from django import forms

DECADE_LIST = [
    ('1900', '1900'),
    ('1930', '1930'),
    ('1940', '1940'),
    ('1950', '1950'),
    ('1960', '1960'),
    ('1970', '1970'),
    ('1980', '1980'),
    ('1990', '1990'),
    ('2000', '2000'),
    ('2010', '2010'),
    ('2020', '2020'),
]


class Film(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    director = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='movie-posters/')
    decade_fk = models.ForeignKey('Decade', on_delete=models.PROTECT, to_field='decade')

    def __str__(self):
        return self.title


class Decade(models.Model):
    decade = models.CharField(max_length=50, choices=DECADE_LIST, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title