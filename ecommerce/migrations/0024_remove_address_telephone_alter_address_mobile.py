# Generated by Django 4.2.6 on 2023-11-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0023_alter_address_mobile_alter_address_telephone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='telephone',
        ),
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
