from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ShoppingCart
from ShoppingCartItem.models import ShoppingCartItem
from ProductsItem.models import ProductItem,ProductImage
from SiteUser.models import SiteUser
from Products.models import Product


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    site_user = get_object_or_404(SiteUser, user=request.user)
    cart = get_object_or_404(ShoppingCart, site_user=site_user)
    cart_items = cart.items.all()  
    products_data = []

    for item in cart_items:
        product_item = get_object_or_404(ProductItem, id=item.product_id)
        product = product_item.product  #
        existing_product = next((p for p in products_data if p['product_id'] == product.id), None)
        images = ProductImage.objects.filter(product_item=product_item)
        image_urls = [image.url for image in images]

        product_item_data = {
            "sku": product_item.SKU,
            "price": product_item.price,
            "color": product_item.color,
            "size": product_item.size,
            "qty_in_stock": product_item.qty_in_stock,
            "images": image_urls
        }
        if existing_product:
            existing_product['items'].append(product_item_data)
        else:
            products_data.append({
                "product_id": product.id,
                "product_name": product.name,
                "description": product.description,
                "product_items": [product_item_data]  
            })

    return JsonResponse(products_data, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    site_user = get_object_or_404(SiteUser, user=request.user)
    cart, created = ShoppingCart.objects.get_or_create(site_user=site_user)

    product_id = request.data.get('product_id')  
    product = get_object_or_404(Product, id=product_id) 
    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart,
        product_id=product.id, 
        defaults={
            'product_name': product.name,  
            'status': 'available'  
        }
    )

    if not created:
        pass

    return JsonResponse({
        "message": "Sản phẩm đã được thêm vào giỏ hàng!",
        "product": {
            "id": product.id,
            "productName": product.name,
            "status": cart_item.status,  
        }
    }, status=status.HTTP_201_CREATED)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)

    if cart_item.cart.site_user.user != request.user:
        return JsonResponse({"error": "Bạn không có quyền chỉnh sửa sản phẩm này."}, status=status.HTTP_403_FORBIDDEN)

    qty = int(request.data.get('qty', 0))
    product_item = get_object_or_404(ProductItem, id=cart_item.product_id)

    if qty > product_item.qty_in_stock:
        return JsonResponse({"error": "Số lượng vượt quá số lượng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)

    cart_item.qty = qty
    cart_item.save()

    return JsonResponse({
        "message": "Sản phẩm trong giỏ hàng đã được cập nhật!",
        "product": {
            "id": cart_item.product_id,
            "productName": cart_item.product_name,
            "price": cart_item.price,
            "quantity": cart_item.qty,
        }
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)
    
    if cart_item.cart.site_user.user != request.user:
        return JsonResponse({"error": "Bạn không có quyền xóa sản phẩm này."}, status=status.HTTP_403_FORBIDDEN)

    cart_item.delete()
    
    return JsonResponse({
        "message": "Sản phẩm đã được xóa khỏi giỏ hàng!"
    }, status=status.HTTP_204_NO_CONTENT)
