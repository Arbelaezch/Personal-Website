"""Helpers shared by the smoke tests."""
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

# A valid 1x1 GIF, for ImageField values.
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00"
    b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


def tiny_image(name="test.gif"):
    return SimpleUploadedFile(name, TINY_GIF, content_type="image/gif")


# Templates use {% static %}; production's manifest storage needs collectstatic output,
# so tests use plain static storage and a throw-away MEDIA_ROOT.
_MEDIA = tempfile.mkdtemp(prefix="portfolio-test-media-")


@override_settings(
    MEDIA_ROOT=_MEDIA,
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class SmokeTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(_MEDIA, ignore_errors=True)
