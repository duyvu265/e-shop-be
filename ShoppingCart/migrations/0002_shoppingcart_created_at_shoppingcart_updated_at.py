# Generated by Django 5.1.2 on 2024-10-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
