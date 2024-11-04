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
    attachments = models.FileField(upload_to='chat_attachments/', blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender.user.email} at {self.timestamp}"
