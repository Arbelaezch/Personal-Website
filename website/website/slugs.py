"""Unique slugs for models whose slug is a public URL."""
from django.utils.text import slugify


def unique_slug(instance, source, fallback, field_name="slug"):
    """A slug for `instance` built from `source` that no other row of the same model uses.

    Falls back to `fallback` when the source has nothing sluggable (punctuation, non-Latin text),
    never returns digits only (those would be read as a primary key in URLs), stays within the
    field's max_length and adds -2, -3, ... until it is free.
    """
    max_length = instance._meta.get_field(field_name).max_length
    base = slugify(source)
    if not base:
        base = fallback
    elif base.isdigit():
        base = f"{fallback}-{base}"
    base = base[:max_length].strip("-")

    others = type(instance)._default_manager.all()
    if instance.pk is not None:
        others = others.exclude(pk=instance.pk)

    candidate, number = base, 2
    while others.filter(**{field_name: candidate}).exists():
        suffix = f"-{number}"
        candidate = base[:max_length - len(suffix)].rstrip("-") + suffix
        number += 1
    return candidate
