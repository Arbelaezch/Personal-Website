from django.db import migrations, models
import website.fields


class Migration(migrations.Migration):
    """Additive only. Every new NOT NULL column has a database default, so the previous release
    (which does not know these columns) can still insert rows after a code rollback."""

    dependencies = [
        ('portfolio', '0002_use_ckeditor5_field'),
    ]

    operations = [
        # Not unique yet: 0004 fills the slugs, 0005 adds the unique index.
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, default='', db_default='', max_length=80, db_index=False),
        ),
        migrations.AddField(
            model_name='project',
            name='summary',
            field=models.CharField(blank=True, default='', db_default='', help_text='One line shown in lists and on the home page. Falls back to the GitHub description, then the subtitle.', max_length=200),
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, default='', db_default='', help_text='Short label, for example "Agent pipeline".', max_length=60),
        ),
        migrations.AddField(
            model_name='project',
            name='primary_language',
            field=models.CharField(blank=True, default='', db_default='', max_length=40),
        ),
        migrations.AddField(
            model_name='project',
            name='is_published',
            field=models.BooleanField(db_default=True, default=True, help_text='Unpublished projects are hidden everywhere on the site.'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_featured',
            field=models.BooleanField(db_default=False, default=False, help_text='Featured projects get the prominent spot on the home page. Aim for about five.'),
        ),
        migrations.AddField(
            model_name='project',
            name='github_repo',
            field=models.CharField(blank=True, help_text='"owner/name" of the repository this project is synced from.', max_length=140, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='project',
            name='github_description',
            field=models.CharField(blank=True, default='', db_default='', max_length=350),
        ),
        migrations.AddField(
            model_name='project',
            name='github_pushed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        # No schema change: these only relax form validation (synced projects have no screenshot or write-up).
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, upload_to='projects/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=website.fields.RichTextField(blank=True),
        ),
    ]
