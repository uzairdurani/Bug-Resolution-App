# Generated by Django 3.2.13 on 2022-06-20 09:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('BugApp', '0012_auto_20220620_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='body',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='questionview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 20, 9, 20, 53, 967764, tzinfo=utc)),
        ),
    ]
