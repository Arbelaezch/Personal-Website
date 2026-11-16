"""sitemap.xml: every public page, built from the database."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from films.models import Decade, Movie
from portfolio.models import Project


class PagesSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return ['portfolio', 'projects', 'personal', 'films:top_250']

    def location(self, name):
        return reverse(name)


class ProjectSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Project.objects.filter(is_published=True).exclude(slug='').order_by('pk')

    def lastmod(self, project):
        return project.github_pushed_at


class DecadeSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Decade.objects.order_by('year')

    def location(self, decade):
        return reverse('films:decade_view', kwargs={'year': decade.year})


class MovieSitemap(Sitemap):
    protocol = 'https'

    def items(self):
        return Movie.objects.filter(is_published=True).order_by('pk')

    def location(self, movie):
        return reverse('films:movie_detail', kwargs={'year': movie.get_decade(), 'slug': movie.slug})


SITEMAPS = {'pages': PagesSitemap, 'projects': ProjectSitemap, 'decades': DecadeSitemap, 'movies': MovieSitemap}
