# Generated by Django 5.1 on 2024-10-28 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Banner', '0002_remove_banner_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='end_date',
            field=models.DateTimeField(default='2024-10-28T14:30:00Z'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='start_date',
            field=models.DateTimeField(default='2024-10-28T14:30:00Z'),
            preserve_default=False,
        ),
    ]