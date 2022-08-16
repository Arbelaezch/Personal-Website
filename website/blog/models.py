from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField(config_name='portal_config')
    subject = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title