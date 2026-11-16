from django.conf import settings


def site(request):
    """Values every public template needs for its <head>: the canonical address of the page."""
    return {
        'site_url': settings.SITE_URL,
        'canonical_url': settings.SITE_URL + request.path,
    }
