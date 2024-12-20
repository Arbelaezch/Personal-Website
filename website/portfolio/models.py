from django.db import models
from ckeditor.fields import RichTextField

class Project(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='projects/')
    lessons_learned = RichTextField(blank=True, help_text="Enter each lesson on a new line.")
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    timeline = models.CharField(max_length=200, blank=True, help_text="Jan 2024 - Mar 2024")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title