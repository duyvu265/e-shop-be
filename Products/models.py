from django.db import models
from ProductsCategory.models import ProductCategory

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name