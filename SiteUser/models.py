# users/models.py
from django.db import models
from django.contrib.auth.models import User

class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Mối liên kết 1-1 với mô hình User
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='addresses')  # Mối liên kết nhiều-nhiều với SiteUser
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
      
class UserPaymentMethod(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Payment method for {self.user}"
