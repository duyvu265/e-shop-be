# Generated by Django 5.1 on 2024-11-11 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0010_product_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(default='https://kenh14cdn.com/2020/7/17/brvn-15950048783381206275371.jpg'),
            preserve_default=False,
        ),
    ]