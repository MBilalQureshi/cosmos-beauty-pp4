# Generated by Django 4.2.6 on 2023-11-09 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0032_shipmentdetail_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipmentdetail',
            name='slug',
        ),
    ]
