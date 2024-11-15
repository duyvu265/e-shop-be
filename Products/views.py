from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product
from ProductsItem.models import ProductItem, ProductImage
from ProductsCategory.models import ProductCategory
from django.db.models import Min, Max
import json
import logging


logging.basicConfig(level=logging.DEBUG)

def product_list(request):
    if request.method == 'GET':
        products = Product.objects.prefetch_related(
            'items__images'
        ).values(
            'id',
            'name',
            'description',
            'image_url',
            'is_active',
            'created_at',
            'updated_at',
            'category__id',
            'category__category_name',
            'brand',
            'title'
           
        )

        product_list = []
        for product in products:
            image_urls = []
            items = ProductItem.objects.filter(product_id=product['id'])
            price = items.aggregate(min_price=Min('price'))['min_price'] if items.exists() else None
            for item in items:
                if item.images.exists():
                    image_urls.extend([img.url for img in item.images.all()])

            product_data = {
                'id': product['id'],
                'name': product['name'],
                'description': product['description'],
                'image_url': product['image_url'],
                'is_active': product['is_active'],
                'created_at': product['created_at'],
                'updated_at': product['updated_at'],
                'brand': product['brand'],
                'price': price,
                'title': product['title'],
                
                'category': {
                    'id': product['category__id'],
                    'category_name': product['category__category_name']
                },
                'images': image_urls, 
            }
            product_list.append(product_data)

        return JsonResponse(product_list, safe=False)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)


def create_product(request):
    if request.method == 'POST':
        required_fields = ['category_id', 'name', 'description', 'product_images', 'product_items','brand','title']
        try:
            data = json.loads(request.body)

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing fields: ' + ', '.join(missing_fields)}, status=400)

            category_id = data['category_id']
            name = data['name']
            description = data['description']
            brand = data['brand']
            title = data['title']
            category = get_object_or_404(ProductCategory, id=category_id)

            product = Product(category=category, name=name, description=description,brand=brand, title=title)
            product.save()

            product_items = data.get('product_items', [])
            product_images = data.get('product_images', [])

            created_images = []
            for item in product_items:
                product_item = ProductItem.objects.create(
                    product=product,
                    SKU=item['SKU'],
                    qty_in_stock=item['qty_in_stock'],
                    price=item['price'],
                    color=item.get('color', ''),
                    size=item.get('size', '')
                )
                for image_url in product_images:
                    created_images.append(ProductImage(product_item=product_item, url=image_url))
            ProductImage.objects.bulk_create(created_images)

            return JsonResponse({'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)


def get_product_by_id(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        product_items = []
        for item in product.items.all():
            product_images = {f'image{i+1}': {'url': image.url} for i, image in enumerate(item.images.all())}
            product_items.append({
                'id': item.id,
                'SKU': item.SKU,
                'qty_in_stock': item.qty_in_stock,
                'price': item.price,
                'color': item.color,
                'size': item.size,
                'product_images': product_images,             
            })

        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'brand': product.brand,
            'title': product.title,
            'image_url': product.image_url,
            'category': {
                'id': product.category.id,
                'category_name': product.category.category_name
            },
            'product_items': product_items,
            'is_active': product.is_active,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        return JsonResponse(product_data, status=200)
    
    return JsonResponse({'error': 'Invalid request method!'}, status=400)


def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'PUT':
        required_fields = ['name', 'description', 'category_id', 'product_items','brand',"title"]
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
    product_items = product.items.all()
    prices_with_tax = []

    for item in product_items:
        tax_rate = 0.1
        total_price = item.price + (item.price * tax_rate)
        prices_with_tax.append({
            'product_item_id': item.id,
            'product_item_SKU': item.SKU,
            'total_price_with_tax': total_price,
        })

    return JsonResponse(prices_with_tax, safe=False)
