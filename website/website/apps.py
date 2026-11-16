from django.apps import AppConfig
from django.db.models.signals import post_save


class WebsiteConfig(AppConfig):
    """The project package as an app, so its template tags and management commands are found."""
    name = 'website'

    def ready(self):
        from django.apps import apps
        from website import images
        for label in images.WIDTHS:
            post_save.connect(images.on_save, sender=apps.get_model(label), dispatch_uid=f'resize-{label}')
