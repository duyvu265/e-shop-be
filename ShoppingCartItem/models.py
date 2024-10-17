from django.db import models
from ShoppingCart.models import ShoppingCart
from ProductsItem.models import ProductItem
from django.core.exceptions import ValidationError

class ShoppingCartItem(models.Model):
    STATUS_CHOICES = [
        ('available', 'Có sẵn'),
        ('out_of_stock', 'Đã hết hàng'),
        ('preorder', 'Đặt trước'),
    ]
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, related_name='cart_items', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  
    notes = models.TextField(blank=True, null=True)  

    def clean(self):
        if self.qty > self.product_item.qty_in_stock:
            raise ValidationError("Số lượng trong giỏ hàng không thể lớn hơn số lượng trong kho.")

    def __str__(self):
     if self.product_item and self.product_item.product:
        return f"{self.product_item.product.name} - {self.qty} - {self.status}"
     return "ShoppingCartItem"
