from django.db import models
from SiteUser.models import SiteUser

# Mô hình giỏ hàng
class ShoppingCart(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='shopping_cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo giỏ hàng
    updated_at = models.DateTimeField(auto_now=True)      # Thời gian cập nhật giỏ hàng

    def __str__(self):
        return f"Shopping Cart for {self.site_user.user.username}"

