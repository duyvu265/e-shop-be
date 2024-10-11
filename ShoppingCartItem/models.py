from django.db import models
from ShoppingCart.models import ShoppingCart
from ProductsItem.models import ProductItem
from django.core.exceptions import ValidationError
# Create your models here.
# Mô hình sản phẩm trong giỏ hàng
class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, related_name='cart_items', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

    def clean(self):
        if self.qty > self.product_item.qty_in_stock:
            raise ValidationError("Số lượng trong giỏ hàng không thể lớn hơn số lượng trong kho.")