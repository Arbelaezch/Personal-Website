from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_fill_project_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, default='', db_default='', help_text='The URL for this project. Leave empty to build it from the title; changing it moves the page.', max_length=80, unique=True),
        ),
    ]
