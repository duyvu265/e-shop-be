from rest_framework import serializers
from .models import ShoppingCartItem
from ShoppingCart.models import ShoppingCart
from ProductsItem.models import ProductItem

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ['id', 'site_user', 'created_at']  # Thay đổi các trường này theo model của bạn

class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['id', 'name', 'price', 'qty_in_stock']  # Thay đổi các trường này theo model của bạn

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    cart = ShoppingCartSerializer(read_only=True)
    product_item = ProductItemSerializer(read_only=True)

    class Meta:
        model = ShoppingCartItem
        fields = ['cart', 'product_item', 'qty']

    def validate_qty(self, value):
        """
        Check that the quantity does not exceed available stock.
        """
        product_item = self.context['request'].data.get('product_item')
        if product_item:
            product = ProductItem.objects.get(id=product_item)
            if value > product.qty_in_stock:
                raise serializers.ValidationError("Số lượng trong giỏ hàng không thể lớn hơn số lượng trong kho.")
        return value
