from django.db import models
from SiteUser.models import SiteUser, Address, UserPaymentMethod
from Orders.models import OrderStatus

# Mô hình đơn hàng
class ShopOrder(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(UserPaymentMethod, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=100)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)  # Thời gian giao hàng ước tính
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Phí giao hàng
    completed_at = models.DateTimeField(null=True, blank=True)  # Ngày hoàn thành

    def __str__(self):
        return f"Order {self.id} for {self.site_user.username} - Total: {self.order_total}"
