# Generated by Django 5.1 on 2024-10-15 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteUser', '0002_address_is_primary_address_notes_siteuser_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
