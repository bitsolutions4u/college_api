# Generated by Django 4.0.4 on 2023-07-31 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masters', '0050_customer_stuabroadcountry_customer_stuabroadpassport_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='eabroadvalidfrom',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='eabroadvalidto',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
