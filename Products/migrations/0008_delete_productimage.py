# Generated by Django 5.1 on 2024-10-17 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_remove_product_price_remove_product_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
