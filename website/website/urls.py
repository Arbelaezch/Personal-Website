from django.contrib import admin
from django.urls import include, path, re_path
from website import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('portfolio.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('api.urls')),

    path('blog/', include('blog.urls')),
    path('films/', include('films.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

