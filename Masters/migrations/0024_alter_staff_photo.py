# Generated by Django 4.0.3 on 2023-05-27 14:29

import Masters.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0023_alter_staff_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='photo',
            field=models.ImageField(blank=True, default='bill_pic', null=True, upload_to=Masters.models.images_upload_to),
        ),
    ]
