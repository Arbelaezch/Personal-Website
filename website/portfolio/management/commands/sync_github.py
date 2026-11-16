"""Refresh projects and pipeline activity from GitHub (see portfolio/github.py).

    manage.py sync_github --dry-run    print what would change, write nothing
    manage.py sync_github              run both sections
    manage.py sync_github --only projects|pipeline

Exits non-zero if a section failed. A failed section changes nothing, so the site keeps what it had.
"""
from django.core.management.base import BaseCommand, CommandError

from portfolio import github

SECTIONS = {'projects': github.sync_projects, 'pipeline': github.sync_pipeline}


class Command(BaseCommand):
    help = "Sync portfolio projects and pipeline activity from GitHub."

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help="Print what would change and write nothing.")
        parser.add_argument('--only', choices=sorted(SECTIONS), help="Run one section only.")

    def handle(self, *args, dry_run=False, only=None, **options):
        failed = []
        for name, run in SECTIONS.items():
            if only in (None, name) and not run(self.stdout.write, dry_run=dry_run):
                failed.append(name)
        if dry_run:
            self.stdout.write("Dry run: nothing was written.")
        if failed:
            raise CommandError(f"GitHub sync failed for: {', '.join(failed)}")
