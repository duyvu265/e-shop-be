# Generated by Django 5.1 on 2024-10-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCartItem', '0003_remove_shoppingcartitem_product_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='qty',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
