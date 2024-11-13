# Generated by Django 5.1 on 2024-11-08 09:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0004_chatsession_message_delete_chat'),
        ('SiteUser', '0007_alter_siteuser_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_sent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('received', 'Received'), ('seen', 'Seen')], default='sent', max_length=10),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Chat.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='SiteUser.siteuser')),
            ],
        ),
        migrations.CreateModel(
            name='TypingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_typing', models.BooleanField(default=False)),
                ('chat_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typing_status', to='Chat.chatsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typing_status', to='SiteUser.siteuser')),
            ],
        ),
    ]