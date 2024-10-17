from django.db import models
from Products.models import Product
from django.core.exceptions import ValidationError
class ProductItem(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    SKU = models.CharField(max_length=100, unique=True)
    qty_in_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)

    def clean(self):
        if self.qty_in_stock < 0:
            raise ValidationError("Số lượng trong kho không thể nhỏ hơn 0.")
    
    def __str__(self):
        return self.product.name  