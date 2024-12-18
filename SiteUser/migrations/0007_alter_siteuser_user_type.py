# Generated by Django 5.1 on 2024-11-01 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteUser', '0006_siteuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('super_admin', 'Super Admin'), ('customer', 'Customer'), ('manager', 'manager'), ('staff', 'Staff')], default='customer', max_length=20),
        ),
    ]
