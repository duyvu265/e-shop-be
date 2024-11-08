from django.db import models
from SiteUser.models import SiteUser

class ChatSession(models.Model):
    participants = models.ManyToManyField(SiteUser, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat session {self.id} started at {self.created_at}"

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
