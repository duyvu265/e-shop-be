# admin.py
from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category',  'get_first_image')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductImageInline]

    def get_first_image(self, obj):
        if obj.images.exists():
            return obj.images.first().url  
        return "No Image"

    get_first_image.short_description = 'Product Image'
