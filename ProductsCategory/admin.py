from django.contrib import admin
from .models import ProductCategory

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name','image_url')  
    search_fields = ('category_name',)  
