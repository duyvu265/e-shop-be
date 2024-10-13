from django.db import models
from ShopOrder.models import ShopOrder
from ProductsItem.models import ProductItem
from django.core.exceptions import ValidationError

# Mô hình chi tiết đơn hàng
class OrderLine(models.Model):
    order = models.ForeignKey(ShopOrder, related_name='order_lines', on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, related_name='order_lines', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Giảm giá

    def clean(self):
        if self.qty > self.product_item.qty_in_stock:
            raise ValidationError("Số lượng trong đơn hàng không thể lớn hơn số lượng trong kho.")

    def __str__(self):
        return f"OrderLine {self.id}: {self.product_item.name} - Qty: {self.qty} - Price: {self.price} - Discount: {self.discount}"
