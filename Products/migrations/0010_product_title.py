# Generated by Django 5.1 on 2024-10-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0009_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='title product', max_length=255),
            preserve_default=False,
        ),
    ]