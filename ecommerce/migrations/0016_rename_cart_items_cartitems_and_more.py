# Generated by Django 4.2.6 on 2023-10-25 19:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0015_remove_confirmed_order_details_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='cart_items',
            new_name='CartItems',
        ),
        migrations.RenameModel(
            old_name='confirmed_order_details',
            new_name='ConfirmedOrderDetails',
        ),
        migrations.RenameModel(
            old_name='UserPaymnet',
            new_name='UserPayment',
        ),
    ]
