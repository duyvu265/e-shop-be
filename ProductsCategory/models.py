from django.db import models

# Create your models here.
# Mô hình danh mục sản phẩm
class ProductCategory(models.Model):
    parent_category = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='subcategories'
    )
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name