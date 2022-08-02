from django.contrib import admin
from django.urls import include, path, re_path
from website import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path('film/', include('movies.urls')),
    path('food/', include('food.urls')),
    path('portfolio/', include('portfolio.urls')),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

