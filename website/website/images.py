"""Smaller copies of uploaded images for the pages that show them (issue #86).

An upload is never changed. For each width a page needs, a WebP copy is written next to the uploads
under media/resized/<width>/..., and templates ask for it with the `resized` filter. Until a copy
exists (a fresh upload on an old release, a failed conversion) the filter returns the original, so
nothing ever breaks: the page is only heavier.
"""
import logging
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

QUALITY = 82
PREFIX = 'resized'

# Model -> widths its pages use, at twice the displayed size for sharp screens.
#   200  Top 250 thumbnails (shown 100 px wide)
#   500  poster grid on decade pages (cards up to about 250 px)
#   600  poster on a movie page (300 px)
#  1600  screenshot on a project page (full width of the 1180 px column)
WIDTHS = {
    'films.Movie': [200, 500, 600],
    'portfolio.Project': [1600],
}

_known = set()  # resized files seen on disk by this process, to avoid a stat per image per request


def resized_name(name, width):
    return str(PurePosixPath(PREFIX) / str(width) / PurePosixPath(name).with_suffix('.webp'))


def resized_url(image, width):
    """URL of the resized copy of an ImageField value, or of the original while there is no copy."""
    if not image:
        return ''
    name = resized_name(image.name, width)
    if name in _known or default_storage.exists(name):
        _known.add(name)
        return default_storage.url(name)
    return image.url


def make_resized(image, width, force=False):
    """Write the resized copy. Returns its storage name, or None if there is nothing to do or it cannot be read."""
    if not image:
        return None
    name = resized_name(image.name, width)
    if default_storage.exists(name):
        if not force:
            return None
        default_storage.delete(name)
    try:
        with default_storage.open(image.name, 'rb') as source:
            picture = Image.open(source)
            if getattr(picture, 'is_animated', False):
                return None  # an animation would lose its frames; keep the original
            picture = ImageOps.exif_transpose(picture)
            if picture.mode not in ('RGB', 'RGBA'):
                picture = picture.convert('RGBA' if 'transparency' in picture.info or picture.mode in ('LA', 'PA') else 'RGB')
            if picture.width > width:  # never enlarge
                picture = picture.resize((width, round(picture.height * width / picture.width)), Image.LANCZOS)
            out = BytesIO()
            picture.save(out, 'WEBP', quality=QUALITY, method=6)
    except Exception as error:  # a missing or broken upload must not break a save or the backfill
        logger.warning('could not resize %s: %s', image.name, error)
        return None
    saved = default_storage.save(name, ContentFile(out.getvalue()))
    _known.add(saved)
    return saved


def resize_for(instance, force=False):
    """Make every copy this object's pages need. Returns the names written."""
    widths = WIDTHS.get(instance._meta.label, [])
    written = [make_resized(instance.image, width, force=force) for width in widths]
    return [name for name in written if name]


def on_save(sender, instance, **kwargs):
    resize_for(instance)
