from django.db import models

# Mô hình giảm giá
class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)  # Mô tả chi tiết về chương trình giảm giá
    applicable_to = models.CharField(max_length=100, blank=True, null=True)  # Đối tượng áp dụng

    def __str__(self):
        return f"Discount Code: {self.code} - Amount: {self.amount} - Description: {self.description}"
