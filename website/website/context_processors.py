from django.conf import settings


def site(request):
    """Values every public template needs for its <head>: the canonical address of the page."""
    from portfolio.models import Resume
    return {
        # One small query per page, so the buttons appear the moment a resume is uploaded.
        'has_resume': Resume.objects.filter(is_current=True).exists(),
        'site_url': settings.SITE_URL,
        'canonical_url': settings.SITE_URL + request.path,
    }
