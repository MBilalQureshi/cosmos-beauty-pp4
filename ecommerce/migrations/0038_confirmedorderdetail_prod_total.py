# Generated by Django 4.2.6 on 2023-11-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0037_userbill_user_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmedorderdetail',
            name='prod_total',
            field=models.DecimalField(decimal_places=2, default=1.1, max_digits=6),
            preserve_default=False,
        ),
    ]
