"""Write the smaller copies of uploaded images that pages use (see website/images.py).

New uploads get their copies when they are saved. This command fills in everything uploaded before
that, and can rebuild all copies after a change to the sizes or quality.

    manage.py resize_images --dry-run     list what is missing
    manage.py resize_images               write the missing copies
    manage.py resize_images --force       rebuild every copy

Originals are never modified or deleted.
"""
from django.apps import apps
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from website import images


class Command(BaseCommand):
    help = "Write resized WebP copies of uploaded images. Originals are untouched."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help="List what would be written and write nothing.")
        parser.add_argument('--force', action='store_true', help="Rebuild copies that already exist.")

    def handle(self, *args, dry_run=False, force=False, **options):
        written = original_bytes = resized_bytes = 0
        for label, widths in images.WIDTHS.items():
            for instance in apps.get_model(label).objects.exclude(image='').order_by('pk'):
                missing = [w for w in widths if force or not default_storage.exists(images.resized_name(instance.image.name, w))]
                if not missing:
                    continue
                if dry_run:
                    self.stdout.write(f"would write {instance.image.name}: {', '.join(map(str, missing))}")
                    written += len(missing)
                    continue
                names = images.resize_for(instance, force=force)
                if not names:
                    self.stdout.write(f"skipped {instance.image.name} (missing, unreadable or animated)")
                    continue
                written += len(names)
                try:
                    original = default_storage.size(instance.image.name)
                except OSError:
                    original = 0
                sizes = [default_storage.size(name) for name in names]
                original_bytes += original
                resized_bytes += max(sizes)
                self.stdout.write(
                    f"{instance.image.name}: {original // 1024} KB -> " + ", ".join(f"{s // 1024} KB" for s in sizes))
        verb = "would write" if dry_run else "wrote"
        self.stdout.write(f"{verb} {written} files")
        if resized_bytes:
            self.stdout.write(
                f"originals {original_bytes / 1e6:.1f} MB, largest copies {resized_bytes / 1e6:.1f} MB "
                f"({100 - 100 * resized_bytes / max(original_bytes, 1):.0f}% smaller)")
