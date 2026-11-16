import re

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from website.fields import RichTextField
from website.slugs import unique_slug


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=80, unique=True, blank=True, default='', db_default='',
        help_text="The URL for this project. Leave empty to build it from the title; changing it moves the page.")
    subtitle = models.CharField(max_length=200, blank=True)
    summary = models.CharField(
        max_length=200, blank=True, default='', db_default='',
        help_text="One line shown in lists and on the home page. Falls back to the GitHub description, then the subtitle.")
    category = models.CharField(max_length=60, blank=True, default='', db_default='', help_text='Short label, for example "Agent pipeline".')
    primary_language = models.CharField(max_length=40, blank=True, default='', db_default='')
    description = RichTextField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True)
    lessons_learned = RichTextField(blank=True, help_text="Enter each lesson on a new line.")
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    timeline = models.CharField(max_length=200, blank=True, help_text="Jan 2024 - Mar 2024")

    is_published = models.BooleanField(default=True, db_default=True, help_text="Unpublished projects are hidden everywhere on the site.")
    is_featured = models.BooleanField(default=False, db_default=False, help_text="Featured projects get the prominent spot on the home page. Aim for about five.")

    # Filled by the GitHub sync. NULL (not '') when the project has no repository, so the unique index allows many of them.
    github_repo = models.CharField(
        max_length=140, unique=True, null=True, blank=True,
        help_text='"owner/name" of the repository this project is synced from.')
    github_description = models.CharField(max_length=350, blank=True, default='', db_default='')
    github_pushed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # An existing slug is never rebuilt when the title changes: URLs must not move.
        if not self.slug:
            self.slug = unique_slug(self, self.title, fallback="project")
        if not self.github_repo:
            self.github_repo = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if not self.slug:
            # Only a row inserted by the release before slugs existed (after a rollback) has none.
            # Its id link gives it one on the first visit.
            return reverse('project_by_id', kwargs={'pk': self.pk})
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def display_summary(self):
        return self.summary or self.github_description or self.subtitle

    @property
    def display_year(self):
        """The year shown in project lists: last GitHub activity, else the last year named in the timeline."""
        if self.github_pushed_at:
            return str(self.github_pushed_at.year)
        years = re.findall(r'\b(?:19|20)\d{2}\b', self.timeline)
        return years[-1] if years else ''

    @property
    def meta_label(self):
        """"Agent pipeline · Python", or whichever of the two is set."""
        return ' · '.join(part for part in [self.category, self.primary_language] if part)


RESUME_MAX_BYTES = 2 * 1024 * 1024


def validate_resume_file(upload):
    """A real PDF of a sensible size: the extension alone can be faked."""
    if upload.size > RESUME_MAX_BYTES:
        raise ValidationError("The resume must be smaller than 2 MB.")
    start = upload.read(5)
    upload.seek(0)
    if start != b"%PDF-":
        raise ValidationError("This file is not a PDF.")


class Resume(models.Model):
    """The resume visitors download at /resume/. Uploaded in the admin and never committed:
    the repository is public and the file holds personal data."""
    file = models.FileField(
        upload_to='resume/',
        validators=[FileExtensionValidator(['pdf']), validate_resume_file],
        help_text="PDF, under 2 MB. Visitors always receive it as Christian-Arbelaez-Resume.pdf.")
    is_current = models.BooleanField(default=True, help_text="The one visitors download. Marking a resume current unmarks the others.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume uploaded {self.uploaded_at:%Y/%m/%d}" if self.uploaded_at else "Resume"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_current:
            Resume.objects.exclude(pk=self.pk).filter(is_current=True).update(is_current=False)

    def delete(self, *args, **kwargs):
        # Files under /media/ are served directly by nginx: an old resume must not stay downloadable.
        stored = self.file
        result = super().delete(*args, **kwargs)
        if stored:
            stored.delete(save=False)
        return result

    @classmethod
    def current(cls):
        return cls.objects.filter(is_current=True).first()
