from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import Movie, Decade, Top250Entry


class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'decade', 'created_at']

class DecadeAdmin(admin.ModelAdmin):
    filter_horizontal = ('favorite_movies',)  # Makes it easier to select favorite movies
    list_display = ('year', 'title', 'get_favorite_count')
    
    def get_favorite_count(self, obj):
        return obj.favorite_movies.count()
    get_favorite_count.short_description = 'Number of Favorites'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "favorite_movies":
            # Get the current decade instance
            if request.resolver_match.kwargs.get('object_id'):
                decade = self.get_object(request, request.resolver_match.kwargs['object_id'])
                if decade:
                    # Filter movies using get_decade()
                    kwargs["queryset"] = Movie.objects.filter(
                        release_year__in=[
                            year for year in range(decade.year, decade.year + 10)
                            if Movie.get_decade(Movie(release_year=year)) == decade.year
                        ]
                    )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class Top250EntryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('rank', 'movie', 'last_modified')
    search_fields = ('movie__title',)
    list_select_related = ('movie',)
    list_per_page = 250
    autocomplete_fields = ['movie']



admin.site.register(Top250Entry, Top250EntryAdmin)
admin.site.register(Decade, DecadeAdmin)
admin.site.register(Movie, MovieAdmin)