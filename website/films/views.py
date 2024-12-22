from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.urls import reverse
from django.http import Http404
import logging
logger = logging.getLogger(__name__)

from .models import Movie, Decade, Top250Entry


def top250_view(request):
    # Get all Top 250 entries with their related movies
    entries = Top250Entry.objects.select_related(
        'movie'
    ).all()  # ordering by rank is handled by model Meta
    
    # Get all decades for navigation
    decades = Decade.objects.all()
    
    context = {
        'entries': entries,
        'decades': decades,
    }
    
    return render(request, 'films/top250.html', context)


def decade_view(request, year):
    # Validate year is reasonable
    if not (1800 <= year <= 2100):  # Adjust range as needed
        raise Http404("Invalid decade")
    
    # Get the specific decade
    decade = get_object_or_404(Decade, year=year)

    # Special case for 1900s
    if year == 1900:
        end_year = 1929  # Include all films from 1900-1929
    else:
        end_year = year + 9
    
    # Get all movies from this decade
    movies = Movie.objects.filter(
        release_year__gte=year,
        release_year__lte=end_year,
        is_published=True
    ).select_related(
        'decade'
    ).order_by('release_year', 'title')
    
    # Get favorite movies for this decade
    favorite_movies = decade.favorite_movies.filter(
        is_published=True
    ).select_related('decade')
    
    # Get all decades for navigation
    all_decades = Decade.objects.all()
    
    context = {
        'decade': decade,
        'movies': movies or [],  # Provide empty list as fallback
        'favorite_movies': favorite_movies or [],
        'all_decades': all_decades or [],
        'year': year,
    }
    
    return render(request, 'films/decade.html', context)


def movie_detail_view(request, year, slug):
    # Get the movie
    movie = get_object_or_404(
        Movie.objects.select_related('decade'),
        slug=slug,
        is_published=True
    )
    
    # Validate that the movie belongs to the correct decade
    movie_decade = movie.get_decade()
    if movie_decade != year:
        # Redirect to the correct decade URL
        return redirect(
            reverse('movie_detail', kwargs={
                'year': movie_decade,
                'slug': slug
            })
        )
    
    # Get related movies (same genre and decade)
    # related_movies = Movie.objects.filter(
    #     genre=movie.genre,
    #     release_year__gte=year,
    #     release_year__lte=year + 9,
    #     is_published=True
    # ).exclude(
    #     id=movie.id
    # ).select_related(
    #     'decade'
    # )[:4]
    
    # Check if movie is in Top 250
    try:
        top250_rank = movie.top250_entry.rank
    except Top250Entry.DoesNotExist:
        top250_rank = None
    
    # Get decade object for additional context
    decade = get_object_or_404(Decade, year=year)
    # Add to context data when working properly.
    # 'related_movies': related_movies,

    context = {
        'movie': movie,
        'decade': decade,
        'top250_rank': top250_rank,
        'year': year,
    }
    
    return render(request, 'films/movie_detail.html', context)