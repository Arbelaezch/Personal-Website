from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Article(models.Model):
    SUBJECT_CHOICES = [
        ("META", "META"),
        ("Programming", "Programming"),
        ("Film", "Film"),
        ("Music", "Music"),
        ("Other", "Other"),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="")
    body = RichTextUploadingField(config_name='portal_config')
    subject = models.CharField(choices=SUBJECT_CHOICES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_formatted_date(self):
        return self.created_at.strftime("%d %B %Y")
    
    @classmethod
    def get_reverse_chronological_order(cls):
        return cls.objects.order_by('-created_at')

    def __str__(self):
        return self.title

