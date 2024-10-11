from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

# Mô hình trạng thái đơn hàng
class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status




















