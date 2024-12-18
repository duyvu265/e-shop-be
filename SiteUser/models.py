from django.db import models
from django.contrib.auth.models import User
from Products.models import Product

class SiteUser(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
        ('customer', 'Customer'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_sent_at = models.DateTimeField(blank=True, null=True)  

    def __str__(self):
        return self.user.username

class LikedProduct(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='liked_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} likes {self.product}"

class Address(models.Model):
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['site_user'], condition=models.Q(is_primary=True), name='unique_primary_address_per_user')
        ]

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"

class UserPaymentMethod(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    cardholder_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment method for {self.user}"
