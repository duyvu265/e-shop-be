# Generated by Django 5.1 on 2024-11-15 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteUser', '0008_alter_siteuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='verification_code_sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('super_admin', 'Super Admin'), ('customer', 'Customer'), ('manager', 'Manager'), ('staff', 'Staff')], default='customer', max_length=20),
        ),
    ]