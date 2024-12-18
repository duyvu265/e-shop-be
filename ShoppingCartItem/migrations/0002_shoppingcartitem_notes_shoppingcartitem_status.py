# Generated by Django 5.1.2 on 2024-10-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingCartItem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcartitem',
            name='status',
            field=models.CharField(choices=[('available', 'Có sẵn'), ('out_of_stock', 'Đã hết hàng'), ('preorder', 'Đặt trước')], default='available', max_length=20),
        ),
    ]
