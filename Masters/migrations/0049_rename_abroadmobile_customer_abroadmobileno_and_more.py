# Generated by Django 4.0.4 on 2023-07-30 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0048_customer_abroadmobile_customer_fatherabroadmobile_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='abroadMobile',
            new_name='abroadmobileno',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='fatherAbroadMobile',
            new_name='fatherabroadmobileno',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='motherAbroadMobile',
            new_name='motherabroadmobileno',
        ),
    ]
