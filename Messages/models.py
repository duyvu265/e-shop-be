from django.db import models
from SiteUser.models import SiteUser
from django.utils import timezone
from datetime import timedelta


class ChatSession(models.Model):
    user = models.ForeignKey(SiteUser, related_name='user_chat_sessions', on_delete=models.CASCADE)
    admin = models.ForeignKey(SiteUser, related_name='admin_chat_sessions', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat session between {self.user.user.email} and {self.admin.user.email} started at {self.created_at}"
    admin = models.ForeignKey(SiteUser, related_name='admin_chat_sessions', on_delete=models.SET_NULL, null=True)
    customer = models.OneToOneField(SiteUser, related_name='customer_chat_session', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat session {self.id} between {self.customer.user.email} and admin started at {self.created_at}"

    def add_admin_participant(self):
        admin_user = SiteUser.objects.filter(is_admin=True).first()
        if admin_user:
            self.admin = admin_user
            self.save()

    def add_user_participant(self, user):
        self.user = user
        self.save()



class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(SiteUser, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=True)
    attachments = models.FileField(upload_to='chat_attachments/', blank=True, null=True)

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('seen', 'Seen')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')

    def __str__(self):
        return f"Message from {self.sender.user.email} at {self.timestamp}"

    def notify_new_message(self):
        recipient = self.chat_session.user if self.sender != self.chat_session.user else self.chat_session.admin
        Notification.objects.create(
            user=recipient,
            message=self
        )
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify_new_message()



class TypingStatus(models.Model):
    user = models.ForeignKey(SiteUser, related_name='typing_status', on_delete=models.CASCADE)
    chat_session = models.ForeignKey(ChatSession, related_name='typing_status', on_delete=models.CASCADE)
    is_typing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user.email} is typing in session {self.chat_session.id}"


class Notification(models.Model):
    user = models.ForeignKey(SiteUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.user.email} regarding message {self.message.id}"
