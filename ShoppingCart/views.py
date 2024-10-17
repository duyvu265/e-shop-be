from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import ShoppingCart
from ShoppingCartItem.models import ShoppingCartItem
from ProductsItem.models import Product
from django.contrib.auth.decorators import login_required


@api_view(['GET'])
@login_required  
def get_cart_items(request):
    cart = get_object_or_404(ShoppingCart, site_user__id=request.user.id)
    items = cart.items.all()  
    cart_data = []

    for item in items:
        cart_data.append({
            "_id": item.product_item.id,
            "productName": item.product_item.name,
            "image": [image.url for image in item.product_item.images.all()],
            "price": item.product_item.price,
            "quantity": item.qty,
            "availability": 'available' if item.product_item.quantity > 0 else 'out_of_stock',
            "category": {
                "category_name": item.product_item.category.category_name,
                "image_url": item.product_item.category.image_url
            },
        })

    return JsonResponse({
        "cart_id": cart.id,
        "items": cart_data,
        "subtotal": sum(item.product_item.price * item.qty for item in items)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def add_to_cart(request, cart_id):
    cart = get_object_or_404(ShoppingCart, id=cart_id)
    if cart.site_user != request.user:
        return JsonResponse({"error": "Bạn không có quyền truy cập giỏ hàng này."}, status=status.HTTP_403_FORBIDDEN)
    
    product_id = request.data.get('product_id')
    qty = int(request.data.get('qty'))
    product_item = get_object_or_404(Product, id=product_id)
    if qty > product_item.quantity:
        return JsonResponse({"error": "Số lượng vượt quá số lượng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item, created = ShoppingCartItem.objects.get_or_create(
        cart=cart,
        product_item=product_item,
        defaults={'qty': qty}
    )

    if not created:
        cart_item.qty += qty
        cart_item.save()

    return JsonResponse({
        "message": "Sản phẩm đã được thêm vào giỏ hàng!",
        "product": {
            "_id": product_item.id,
            "productName": product_item.name,
            "image": [image.url for image in product_item.images.all()],
            "price": product_item.price,
            "quantity": cart_item.qty,
            "availability": 'available' if product_item.quantity > 0 else 'out_of_stock',
            "category": {
                "category_name": product_item.category.category_name,
                "image_url": product_item.category.image_url
            }
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)

    if cart_item.cart.site_user != request.user:
        return JsonResponse({"error": "Bạn không có quyền chỉnh sửa sản phẩm này."}, status=status.HTTP_403_FORBIDDEN)

    qty = int(request.data.get('qty'))
    if qty > cart_item.product_item.quantity:
        return JsonResponse({"error": "Số lượng vượt quá số lượng có sẵn."}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.qty = qty
    cart_item.save()

    return JsonResponse({
        "message": "Sản phẩm trong giỏ hàng đã được cập nhật!",
        "product": {
            "_id": cart_item.product_item.id,
            "productName": cart_item.product_item.name,
            "image": [image.url for image in cart_item.product_item.images.all()],
            "price": cart_item.product_item.price,
            "quantity": cart_item.qty,
            "availability": 'available' if cart_item.product_item.quantity > 0 else 'out_of_stock',
            "category": {
                "category_name": cart_item.product_item.category.category_name,
                "image_url": cart_item.product_item.category.image_url
            }
        }
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id)
    if cart_item.cart.site_user != request.user:
        return JsonResponse({"error": "Bạn không có quyền xóa sản phẩm này."}, status=status.HTTP_403_FORBIDDEN)

    product_data = {
        "_id": cart_item.product_item.id,
        "productName": cart_item.product_item.name,
        "image": [image.url for image in cart_item.product_item.images.all()],
        "price": cart_item.product_item.price,
        "quantity": cart_item.qty,
        "availability": 'available' if cart_item.product_item.quantity > 0 else 'out_of_stock',
        "category": {
            "category_name": cart_item.product_item.category.category_name,
            "image_url": cart_item.product_item.category.image_url
        }
    }

    cart_item.delete()
    
    return JsonResponse({
        "message": "Sản phẩm đã được xóa khỏi giỏ hàng!",
        "product": product_data
    }, status=status.HTTP_204_NO_CONTENT)
