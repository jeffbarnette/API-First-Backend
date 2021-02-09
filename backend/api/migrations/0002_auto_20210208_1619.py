# Generated by Django 3.1.6 on 2021-02-08 16:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
    ]
