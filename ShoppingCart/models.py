from django.db import models 
from SiteUser.models import SiteUser

class ShoppingCart(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='shopping_cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
