from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import ShoppingCart
from ShoppingCartItem.models import ShoppingCartItem
from ProductsItem.models import ProductItem

@api_view(['POST'])
def add_to_cart(request, cart_id):
    cart = get_object_or_404(ShoppingCart, id=cart_id)
    product_id = request.data.get('product_id')
    qty = request.data.get('qty')
    product_item = get_object_or_404(ProductItem, id=product_id)
    if qty > product_item.qty_in_stock:
        return JsonResponse({"error": "Số lượng vượt quá số lượng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)
    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart,
        product_item=product_item,
        defaults={'qty': qty}
    )

    if not created:
        cart_item.qty += qty
        cart_item.save()

    return JsonResponse({"message": "Sản phẩm đã được thêm vào giỏ hàng!"}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)
    qty = request.data.get('qty')
    if qty > cart_item.product_item.qty_in_stock:
        return JsonResponse({"error": "Số lượng vượt quá số lượng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)
    cart_item.qty = qty
    cart_item.save()

    return JsonResponse({"message": "Sản phẩm trong giỏ hàng đã được cập nhật!"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({"message": "Sản phẩm đã được xóa khỏi giỏ hàng!"}, status=status.HTTP_204_NO_CONTENT)
