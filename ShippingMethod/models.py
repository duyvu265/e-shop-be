from django.db import models

# Create your models here.
# Mô hình phương thức vận chuyển
class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name