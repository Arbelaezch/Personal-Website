from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Top250Entry(models.Model):
    movie = models.OneToOneField(
        'Movie',
        on_delete=models.CASCADE,
        related_name='top250_entry'
    )
    rank = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rank']
        verbose_name_plural = 'Top 250 Entries'

    def __str__(self):
        return f"#{self.rank} - {self.movie.title}"


class Decade(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    description = RichTextField(config_name='films')
    year = models.IntegerField()
    image = models.ImageField(upload_to='decade_images', blank=True, null=True)
    favorite_movies = models.ManyToManyField('Movie', related_name='favorites_in_decades', blank=True)
    fun_fact = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['year']

    def __str__(self):
        return f"{self.year}s"
    
    @property
    def decade_range(self):
        return f"{self.year}s - {self.year + 9}"
    

class Movie(models.Model):
    GENRES = (
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('romantic-comedy', 'Romantic Comedy'),
        ('sci-fi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('war', 'War'),
        ('western', 'Western'),
        ('documentary', 'Documentary'),
        ('animation', 'Animation'),
        ('musical', 'Musical'),
        ('sport', 'Sport'),
        ('fantasy', 'Fantasy'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text="The URL for this movie")
    synopsis = RichTextField()
    rating = models.IntegerField(blank=True, null=True)
    release_year = models.IntegerField()
    review = RichTextField(config_name='films')
    genre = models.CharField(max_length=100, choices=GENRES)
    director = models.CharField(max_length=100, blank=True, null=True)
    writer = models.CharField(max_length=100, blank=True, null=True)
    actors = models.CharField(max_length=100, blank=True, null=True)
    producer = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    studio = models.CharField(max_length=100, blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)

    decade = models.ForeignKey(
        Decade,
        on_delete=models.SET_NULL,  # If you delete a decade, don't delete the movies
        null=True,
        related_name='movies'
    )
    image = models.ImageField(upload_to='movie_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    @property
    def top250_rank(self):
        try:
            return self.top250_entry.rank
        except Top250Entry.DoesNotExist:
            return None

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_decade(self):
        if 1900 <= self.release_year <= 1929:
            return 1900
        return (self.release_year // 10) * 10

    def save(self, *args, **kwargs):
        if not self.slug:  # If no slug exists, create one from the title
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)