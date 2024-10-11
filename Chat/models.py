from django.db import models
from SiteUser.models import SiteUser, Address
# Create your models here.
# Mô hình trò chuyện giữa khách hàng và người bán
class Chat(models.Model):
    customer = models.ForeignKey(SiteUser, related_name='customer_chats', on_delete=models.CASCADE)
    seller = models.ForeignKey(SiteUser, related_name='seller_chats', on_delete=models.CASCADE)  # Sử dụng SiteUser cho admin
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.customer.user.email} to {self.seller.user.email} at {self.timestamp}"