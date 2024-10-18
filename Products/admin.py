from django.contrib import admin
from .models import Product
from ProductsItem.models import ProductItem, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fk_name = 'product_item'  

class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'get_first_image')
    search_fields = ('name',)
    list_filter = ('category',)
    inlines = [ProductItemInline]

    def get_first_image(self, obj):
        if obj.items.exists():
            first_item = obj.items.first()
            if first_item.images.exists():
                return first_item.images.first().url  
        return "No Image"

    get_first_image.short_description = 'Product Image'
