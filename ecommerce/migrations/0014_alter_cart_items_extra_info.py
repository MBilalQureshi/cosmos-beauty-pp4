# Generated by Django 4.2.6 on 2023-10-25 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_confirmed_order_details_cart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_items',
            name='extra_info',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
