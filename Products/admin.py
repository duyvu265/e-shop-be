# admin.py
from django.contrib import admin
from .models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity', 'get_first_image')  
    search_fields = ('name',)  
    list_filter = ('category',)  

    def get_first_image(self, obj):      
        if obj.images.exists():
            return obj.images.first().image.url  
        return "No Image"

    get_first_image.short_description = 'Product Image'  
