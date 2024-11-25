from django.db import models
from SiteUser.models import SiteUser
from Products.models import Product
from ProductsCategory.models import ProductCategory

class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    applicable_to = models.CharField(max_length=100, blank=True, null=True)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)  
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True)  

    user_group = models.CharField(max_length=20, choices=SiteUser.USER_TYPE_CHOICES, blank=True, null=True)  
    min_quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Discount Code: {self.code} - Amount: {self.amount} - Description: {self.description}"
