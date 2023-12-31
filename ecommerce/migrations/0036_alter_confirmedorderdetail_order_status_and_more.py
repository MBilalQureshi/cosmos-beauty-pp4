# Generated by Django 4.2.6 on 2023-11-11 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0035_alter_userbill_shipment_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmedorderdetail',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'Order Received'), (1, 'Order On way'), (3, 'Order Delieverd')], default=0),
        ),
        migrations.AlterField(
            model_name='confirmedorderdetail',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_confirmed_order', to=settings.AUTH_USER_MODEL),
        ),
    ]
