# Generated by Django 3.2.13 on 2022-06-20 09:38

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('BugApp', '0013_auto_20220620_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='body',
            field=django_quill.fields.QuillField(validators=[django.core.validators.MinLengthValidator(30, 'the field must contain at least 50 characters')]),
        ),
        migrations.AlterField(
            model_name='questionview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 20, 9, 38, 29, 338984, tzinfo=utc)),
        ),
    ]
