from django.db import models
from ShoppingCart.models import ShoppingCart

STATUS_CHOICES = [
    ('available', 'Có sẵn'),
    ('out_of_stock', 'Đã hết hàng'),
    ('preorder', 'Đặt trước'),
]

class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField() 
    product_name = models.CharField(max_length=255) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  
    notes = models.TextField(blank=True, null=True)  
    qty = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.product_name} - {self.status}"
