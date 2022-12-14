# Generated by Django 3.2.13 on 2022-06-14 19:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BugApp', '0007_answers_thumbs'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='thumbs',
            field=models.ManyToManyField(blank=True, default=None, related_name='Qthumbs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answers',
            name='thumbs',
            field=models.ManyToManyField(blank=True, default=None, related_name='Athumbs', to=settings.AUTH_USER_MODEL),
        ),
    ]
