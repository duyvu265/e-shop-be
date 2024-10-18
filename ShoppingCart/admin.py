from django.contrib import admin
from .models import ShoppingCart
from ShoppingCartItem.models import ShoppingCartItem
from ProductsItem.models import ProductItem

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_user', 'created_at', 'updated_at')  
    search_fields = ('site_user__email',)  
    list_filter = ('created_at', 'updated_at')  
    ordering = ('-created_at',)  

class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'get_price', 'get_qty', 'status')

    def get_price(self, obj):
        # Trả về giá từ ProductItem
        product_item = ProductItem.objects.get(id=obj.product_id)
        return product_item.price

    def get_qty(self, obj):
        # Trả về qty từ ProductItem
        product_item = ProductItem.objects.get(id=obj.product_id)
        return product_item.qty

    get_price.short_description = 'Price'
    get_qty.short_description = 'Quantity'
admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)