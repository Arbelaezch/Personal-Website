from django.contrib import admin
from .models import Movie, Decade, Top250Entry
from adminsortable2.admin import SortableAdminMixin


class DecadeAdmin(admin.ModelAdmin):
    filter_horizontal = ('favorite_movies',)  # Makes it easier to select favorite movies
    list_display = ('year', 'title', 'get_favorite_count')
    
    def get_favorite_count(self, obj):
        return obj.favorite_movies.count()
    get_favorite_count.short_description = 'Number of Favorites'


class Top250EntryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('rank', 'movie', 'last_modified')
    search_fields = ('movie__title',)
    list_select_related = ('movie',)
    list_per_page = 250



admin.site.register(Top250Entry, Top250EntryAdmin)
admin.site.register(Decade, DecadeAdmin)
admin.site.register(Movie)