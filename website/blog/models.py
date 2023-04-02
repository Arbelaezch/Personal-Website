from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Article(models.Model):
    SUBJECT_CHOICES = [
        ("Programming", "Programming"),
        ("Film", "Film"),
        ("Music", "Music"),
    ]
    
    
    title = models.CharField(max_length=200)
    body = RichTextUploadingField(config_name='portal_config')
    subject = models.CharField(choices=SUBJECT_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title

