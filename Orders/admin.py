
from django.db import models
from Products.models import Product
from SiteUser.models import SiteUser
from Orders.models import OrderStatus
# Register your models here.
# Mô hình cho đơn hàng
class Order(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=50)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.qty > self.product.qty_in_stock:
            raise ValueError("Quantity cannot be greater than quantity in stock.")
        super().save(*args, **kwargs)