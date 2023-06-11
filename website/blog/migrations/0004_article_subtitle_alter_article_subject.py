# Generated by Django 4.1.6 on 2023-04-02 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_article_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='subtitle',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='subject',
            field=models.CharField(choices=[('META', 'META'), ('Programming', 'Programming'), ('Film', 'Film'), ('Music', 'Music'), ('Other', 'Other')], max_length=50),
        ),
    ]
