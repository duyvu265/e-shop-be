from django.db import models 
from SiteUser.models import SiteUser

# Create your models here.

# Mô hình giỏ hàng
class ShoppingCart(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='shopping_cart', on_delete=models.CASCADE)
