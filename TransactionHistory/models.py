from django.db import models
from SiteUser.models import SiteUser, Address
from ShopOrder.models import ShopOrder
# Create your models here.
# Mô hình lịch sử giao dịch
class TransactionHistory(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='transactions', on_delete=models.CASCADE)
    order = models.ForeignKey(ShopOrder, related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50)  # Thông tin trạng thái thanh toán

    def __str__(self):
        return f"{self.site_user.user.email} - {self.amount} - {self.transaction_date}"