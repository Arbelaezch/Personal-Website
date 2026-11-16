from django import template

from website.images import resized_url

register = template.Library()


@register.filter
def resized(image, width):
    """{{ movie.image|resized:500 }}: the URL of the smaller copy, or of the upload itself until one exists."""
    return resized_url(image, int(width))
