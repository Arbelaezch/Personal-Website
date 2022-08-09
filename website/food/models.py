from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    rating = models.CharField(max_length=3, default='', null=True, blank=True)


    def __str__(self):
        return self.title