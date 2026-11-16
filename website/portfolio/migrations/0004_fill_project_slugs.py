from django.db import migrations
from django.utils.text import slugify

MAX_LENGTH = 80


def fill_slugs(apps, schema_editor):
    """Give every project without a slug a unique one built from its title (same rules as website.slugs)."""
    Project = apps.get_model('portfolio', 'Project')
    taken = set(Project.objects.exclude(slug='').values_list('slug', flat=True))
    for project in Project.objects.filter(slug='').order_by('pk'):
        base = slugify(project.title)
        if not base:
            base = 'project'
        elif base.isdigit():
            base = f'project-{base}'
        base = base[:MAX_LENGTH].strip('-')
        candidate, number = base, 2
        while candidate in taken:
            suffix = f'-{number}'
            candidate = base[:MAX_LENGTH - len(suffix)].rstrip('-') + suffix
            number += 1
        taken.add(candidate)
        project.slug = candidate
        project.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_project_publishing_and_github_fields'),
    ]

    operations = [
        # Reverse is a no-op: the slugs are harmless to the previous release.
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
