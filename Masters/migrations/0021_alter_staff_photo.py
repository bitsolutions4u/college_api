# Generated by Django 4.0.3 on 2023-05-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0020_alter_staff_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='staff/'),
        ),
    ]
