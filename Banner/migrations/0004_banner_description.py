# Generated by Django 5.1 on 2024-10-28 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0003_banner_end_date_banner_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='description',
            field=models.CharField(default='this is a description', max_length=255),
            preserve_default=False,
        ),
    ]
