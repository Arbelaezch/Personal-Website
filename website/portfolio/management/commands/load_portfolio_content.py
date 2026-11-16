"""First content for the redesigned site: which projects are featured, a one-line summary, category
and language for each known project (#100), and draft case studies and a screenshot (#104).

Safe to run more than once. It only fills fields that are empty, creates the listed projects that do
not exist yet, and sets the featured flags only while no project is featured. Text edited in the
admin is never overwritten.

    manage.py load_portfolio_content --dry-run
    manage.py load_portfolio_content
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.content import case_studies
from portfolio.models import Project

CONTENT_DIR = Path(__file__).resolve().parent.parent.parent / 'content'

GITHUB = 'https://github.com/'

# Found by `match` (the slug of an existing project) or by `github_repo`; created when neither exists.
PROJECTS = [
    {
        'title': 'Software Factory', 'github_repo': 'Arbelaezch/software-factory', 'featured': True, 'order': 100,
        'category': 'Agent pipeline', 'primary_language': 'Python',
        'summary': 'A multi-agent delivery pipeline for Claude Code: scouts, a planner, engineers, a reviewer '
                   'from a different lab and a verifier, with human approval and git guardrails.',
        **case_studies.SOFTWARE_FACTORY,
    },
    {
        'title': 'Court Vision', 'github_repo': 'Arbelaezch/court-vision', 'featured': True, 'order': 99,
        'category': 'Browser game', 'primary_language': 'TypeScript',
        'project_url': 'https://arbelaezch.github.io/court-vision/',
        'summary': 'A three.js basketball game that teaches newcomers to read the floor: run real plays as the '
                   'point guard, first against cones, then against defenders who react.',
        'image': 'court-vision.jpg',
        **case_studies.COURT_VISION,
    },
    {
        'title': 'Callback', 'github_repo': 'Arbelaezch/callback', 'featured': True, 'order': 98,
        'category': 'AI application', 'primary_language': 'Python',
        'summary': "Writes a tailored resume and cover letter for a job in the user's own voice, with Claude "
                   'doing narrow, testable tasks inside a Django, Celery and Next.js stack.',
        **case_studies.CALLBACK,
    },
    {
        'match': 'fhir-patient-portal', 'title': 'FHIR Patient Portal',
        'github_repo': 'Arbelaezch/FHIR-patient-portal', 'featured': True,
        'category': 'Healthcare', 'primary_language': 'Python',
        'summary': 'A SMART on FHIR patient dashboard: OAuth2 with PKCE against a healthcare sandbox, with '
                   'access tokens kept server-side so they never reach the browser.',
    },
    {
        'match': 'nba-draft-simulator', 'title': 'NBA Draft Simulator',
        'github_repo': 'Arbelaezch/nba-draft-simulator', 'featured': True,
        'category': 'Mobile game', 'primary_language': 'React Native',
        'summary': 'A React Native NBA draft simulator with 10,000+ downloads on the Google Play Store.',
    },
    {'match': 'habitslots', 'title': 'HabitSlots', 'category': 'Mobile app', 'primary_language': 'TypeScript'},
    {'match': 'algoarena', 'title': 'AlgoArena', 'github_repo': 'Arbelaezch/AlgoArena',
     'category': 'Web app', 'primary_language': 'TypeScript'},
    {'match': 'movie-review-sentiment-analyzer', 'title': 'Movie Review Sentiment Analyzer',
     'github_repo': 'Arbelaezch/imdb-sentiment-analysis', 'category': 'Machine learning', 'primary_language': 'Python'},
    {'match': 'family-food', 'title': 'Family Food', 'github_repo': 'Arbelaezch/family-food',
     'category': 'Web app', 'primary_language': 'JavaScript'},
]

FILL_IF_EMPTY = [
    'summary', 'category', 'primary_language', 'github_repo', 'github_url', 'project_url',
    'problem', 'description', 'ai_usage', 'safety', 'results', 'lessons_learned',
]


class Command(BaseCommand):
    help = "Load the first featured projects and one-line summaries. Fills empty fields only."
    dry_run = False

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help="Print what would change and write nothing.")

    def handle(self, *args, dry_run=False, **options):
        set_flags = not Project.objects.filter(is_featured=True).exists()
        if not set_flags:
            self.stdout.write("Some projects are already featured: leaving every featured flag as it is.")

        self.dry_run = dry_run
        with transaction.atomic():
            for entry in PROJECTS:
                self.apply(entry, set_flags)
            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write("Dry run: nothing was written.")

    def find(self, entry):
        if entry.get('match'):
            project = Project.objects.filter(slug=entry['match']).first()
            if project:
                return project
        if entry.get('github_repo'):
            return Project.objects.filter(github_repo=entry['github_repo']).first()
        return None

    def apply(self, entry, set_flags):
        values = {field: entry[field].strip() for field in FILL_IF_EMPTY if entry.get(field)}
        if entry.get('github_repo'):
            values.setdefault('github_url', GITHUB + entry['github_repo'])

        project = self.find(entry)
        if project is None:
            if entry.get('match'):
                # An existing project that was renamed or removed: do not invent a duplicate.
                self.stdout.write(f"skipped  {entry['title']}: no project with slug {entry['match']!r}")
                return
            project = Project(title=entry['title'], order=entry.get('order', 0), **values)
            project.is_featured = bool(entry.get('featured')) and set_flags
            self.attach_image(project, entry)
            project.save()
            self.stdout.write(f"created  {project.title} (/project/{project.slug}/)" + (", featured" if project.is_featured else ""))
            return

        changed = []
        for field, value in values.items():
            if not getattr(project, field):
                setattr(project, field, value)
                changed.append(field)
        if set_flags and entry.get('featured') and not project.is_featured:
            project.is_featured = True
            changed.append('is_featured')
        if self.attach_image(project, entry):
            changed.append('image')
        if changed:
            project.save()
            self.stdout.write(f"updated  {project.title}: {', '.join(changed)}")
        else:
            self.stdout.write(f"unchanged {project.title}")

    def attach_image(self, project, entry):
        """Give the project the screenshot shipped in portfolio/content/, unless it already has an image."""
        if not entry.get('image') or project.image:
            return False
        if self.dry_run:
            return True  # the database rolls back in a dry run, a file written to media would not
        with open(CONTENT_DIR / entry['image'], 'rb') as source:
            project.image.save(entry['image'], File(source), save=False)
        return True
