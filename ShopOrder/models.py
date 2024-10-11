from django.db import models
from SiteUser.models import SiteUser, Address,UserPaymentMethod
from Orders.models import OrderStatus

# Create your models here.
# Mô hình đơn hàng
class ShopOrder(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(UserPaymentMethod, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=100)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)