from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product
from ProductsCategory.models import ProductCategory
from django.contrib.auth.decorators import login_required
from django.db.models import F 
import json

def product_list(request):
    if request.method == 'GET':
        products = Product.objects.annotate(
            category_name=F('category__category_name')  
        ).values(
            'id', 
            'name', 
            'description', 
            'price', 
            'category_name',  
            'category_id',  
            'product_image', 
            'quantity'
        )
        return JsonResponse(list(products), safe=False)
    return JsonResponse({'error': 'Invalid request method!'}, status=400)


def create_product(request):
    if request.method == 'POST':
        required_fields = ['category_id', 'name', 'description', 'price']  
        try:
            data = json.loads(request.body)

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing fields: ' + ', '.join(missing_fields)}, status=400)

            category_id = data['category_id']
            name = data['name']
            description = data['description']
            price = data['price']
            quantity = data.get('quantity', 0) 
            product_image = request.FILES.get('product_image')

            category = get_object_or_404(ProductCategory, id=category_id)
            product = Product(
                category=category,
                name=name,
                description=description,
                price=price,
                quantity=quantity,  
                product_image=product_image
            )
            product.save()
            return JsonResponse({'message': 'Product created successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'PUT':
        required_fields = ['name', 'description', 'price', 'category_id']  
        try:
            data = json.loads(request.body)

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing fields: ' + ', '.join(missing_fields)}, status=400)

            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)

            category_id = data.get('category_id')
            if category_id:
                category = get_object_or_404(ProductCategory, id=category_id)
                product.category = category

            product.quantity = data.get('quantity', product.quantity)  
            product_image = request.FILES.get('product_image', product.product_image)
            product.product_image = product_image

            product.save()
            return JsonResponse({'message': 'Product updated successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request method!'}, status=400)
def get_product_by_id(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=product_id)
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category_id': product.category.id,  #
            'category_name': product.category.category_name, 
            'product_image': product.product_image.url if product.product_image else None,
            'quantity': product.quantity  
        }
        return JsonResponse(product_data, status=200)
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
