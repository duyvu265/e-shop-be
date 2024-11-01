from django.db import models
from SiteUser.models import SiteUser

class Chat(models.Model):
    customer = models.ForeignKey(SiteUser, related_name='customer_chats', on_delete=models.CASCADE)
    seller = models.ForeignKey(SiteUser, related_name='seller_chats', on_delete=models.CASCADE) 
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  
    attachments = models.FileField(upload_to='chat_attachments/', blank=True, null=True)  
    
    STATUS_CHOICES = [
        ('new', 'Mới'),
        ('in_progress', 'Đang xử lý'),
        ('completed', 'Hoàn thành'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Chat from {self.customer.user.email} to {self.seller.user.email} at {self.timestamp}"
