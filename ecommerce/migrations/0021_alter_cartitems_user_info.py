# Generated by Django 4.2.6 on 2023-11-05 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0020_rename_user_info_wishes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL),
        ),
    ]
