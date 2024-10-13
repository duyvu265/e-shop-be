from django.db import models
from ShoppingCart.models import ShoppingCart
from ProductsItem.models import ProductItem
from django.core.exceptions import ValidationError

# Mô hình sản phẩm trong giỏ hàng
class ShoppingCartItem(models.Model):
    STATUS_CHOICES = [
        ('available', 'Có sẵn'),
        ('out_of_stock', 'Đã hết hàng'),
        ('preorder', 'Đặt trước'),
        # Có thể thêm các trạng thái khác nếu cần
    ]

    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, related_name='cart_items', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # Trạng thái sản phẩm
    notes = models.TextField(blank=True, null=True)  # Ghi chú cho sản phẩm trong giỏ hàng

    def clean(self):
        if self.qty > self.product_item.qty_in_stock:
            raise ValidationError("Số lượng trong giỏ hàng không thể lớn hơn số lượng trong kho.")

    def __str__(self):
        return f"{self.product_item.name} - {self.qty} - {self.status}"
