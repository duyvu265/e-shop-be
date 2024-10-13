from django.db import models
from SiteUser.models import SiteUser

# Mô hình trò chuyện giữa khách hàng và người bán
class Chat(models.Model):
    customer = models.ForeignKey(SiteUser, related_name='customer_chats', on_delete=models.CASCADE)
    seller = models.ForeignKey(SiteUser, related_name='seller_chats', on_delete=models.CASCADE) 
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Theo dõi trạng thái đã đọc của tin nhắn
    attachments = models.FileField(upload_to='chat_attachments/', blank=True, null=True)  # Lưu trữ tệp đính kèm

    def __str__(self):
        return f"Chat from {self.customer.user.email} to {self.seller.user.email} at {self.timestamp}"
