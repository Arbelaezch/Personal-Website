from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.urls import include, path
from website import settings
from django.conf.urls.static import static

from website.sitemaps import SITEMAPS

urlpatterns = [
    path('', include('portfolio.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/', include('api.urls')),

    path('films/', include('films.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

