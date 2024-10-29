from django.db import models
from ProductsCategory.models import ProductCategory

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    brand=models.CharField(max_length=255)
    title=models.CharField(max_length=255)
    

    def __str__(self):
        return self.name


