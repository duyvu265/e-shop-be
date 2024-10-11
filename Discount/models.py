from django.db import models

# Create your models here.
# Mô hình giảm giá
class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Discount Code: {self.code} - Amount: {self.amount}"