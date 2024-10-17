from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product, ProductImage
from ProductsItem.models import ProductItem
from ProductsCategory.models import ProductCategory
import json

def product_list(request):
    if request.method == 'GET':
        products = Product.objects.prefetch_related('images', 'items').values(
            'id',
            'name',
            'description',
            'is_active',
            'created_at',
            'updated_at',
            'category__id',
            'category__category_name'
        )

        product_list = []
        for product in products:
            product_data = {
                'id': product['id'],
                'name': product['name'],
                'description': product['description'],
                'is_active': product['is_active'],
                'created_at': product['created_at'],
                'updated_at': product['updated_at'],
                'category': {
                    'id': product['category__id'],
                    'category_name': product['category__category_name']
                },
                'product_images': {f'image{i+1}': {'url': img.url} for i, img in enumerate(ProductImage.objects.filter(product_id=product['id']))},
                'product_items': [{
                    'id': item.id,
                    'SKU': item.SKU,
                    'qty_in_stock': item.qty_in_stock,
                    'price': item.price,
                    'color': item.color,
                    'size': item.size,
                } for item in ProductItem.objects.filter(product=product['id'])]  
            }
            product_list.append(product_data)

        return JsonResponse(product_list, safe=False)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)

def create_product(request):
    if request.method == 'POST':
        required_fields = ['category_id', 'name', 'description', 'product_images', 'product_items']
        try:
            data = json.loads(request.body)

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing fields: ' + ', '.join(missing_fields)}, status=400)

            category_id = data['category_id']
            name = data['name']
            description = data['description']
            category = get_object_or_404(ProductCategory, id=category_id)

            product = Product(category=category, name=name, description=description)
            product.save()

            product_images = data.get('product_images', [])
            for image_url in product_images:
                ProductImage.objects.create(product=product, url=image_url)
            product_items = data.get('product_items', [])
            for item in product_items:
                ProductItem.objects.create(
                    product=product,
                    SKU=item['SKU'],
                    qty_in_stock=item['qty_in_stock'],
                    price=item['price'],
                    color=item.get('color', ''),
                    size=item.get('size', '')
                )

            return JsonResponse({'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)

def get_product_by_id(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'category_name': product.category.category_name
            },
            'product_images': {f'image{i+1}': {'url': image.url} for i, image in enumerate(product.images.all())},
            'product_items': [{
                'id': item.id,
                'SKU': item.SKU,
                'qty_in_stock': item.qty_in_stock,
                'price': item.price,
                'color': item.color,
                'size': item.size,
            } for item in product.items.all()],
            'is_active': product.is_active,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        return JsonResponse(product_data, status=200)
    
    return JsonResponse({'error': 'Invalid request method!'}, status=400)

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'PUT':
        required_fields = ['name', 'description', 'category_id', 'product_items']
        try:
            data = json.loads(request.body)

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing fields: ' + ', '.join(missing_fields)}, status=400)

            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)

            category_id = data.get('category_id')
            if category_id:
                category = get_object_or_404(ProductCategory, id=category_id)
                product.category = category

            product.save()
            for item_data in data.get('product_items', []):
                item_id = item_data.get('id')
                if item_id:
                    item = get_object_or_404(ProductItem, id=item_id)
                    item.qty_in_stock = item_data.get('qty_in_stock', item.qty_in_stock)
                    item.price = item_data.get('price', item.price)
                    item.color = item_data.get('color', item.color)
                    item.size = item_data.get('size', item.size)
                    item.save()

            return JsonResponse({'message': 'Product updated successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'DELETE':
        product.is_active = False 
        product.save()
        return JsonResponse({'message': 'Product deleted successfully!'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method!'}, status=400)

def calculate_product_price(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    tax_rate = 0.1 
    total_price = product.price + (product.price * tax_rate)
    return JsonResponse({
        'product_id': product.id,
        'product_name': product.name,
        'price': product.price,
        'total_price_with_tax': total_price,
    })
