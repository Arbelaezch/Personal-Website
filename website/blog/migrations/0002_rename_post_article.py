# Generated by Django 4.1.6 on 2023-04-02 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Article',
        ),
    ]
