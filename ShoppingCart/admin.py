from django.contrib import admin
from .models import ShoppingCart
from ShoppingCartItem.models import ShoppingCartItem,ProductItem
from ProductsItem.models import ProductItem

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_user', 'created_at', 'updated_at')  
    search_fields = ('site_user__email',)  
    list_filter = ('created_at', 'updated_at')  
    ordering = ('-created_at',)  

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product_item', 'qty', 'status') 
    search_fields = ('product_item__name',)  
    list_filter = ('status',)  
    ordering = ('-id',)
    
   
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['product_item'].queryset = ProductItem.objects.all()  
        return form
