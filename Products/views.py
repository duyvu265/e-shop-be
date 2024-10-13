from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product
from ProductsCategory.models import ProductCategory
import json

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_id = data['category_id']
            name = data['name']
            description = data['description']
            price = data['price']  
            product_image = data.get('product_image')  

            category = get_object_or_404(ProductCategory, id=category_id)
            product = Product(
                category=category,
                name=name,
                description=description,
                price=price,  
                product_image=product_image
            )
            product.save()
            return JsonResponse({'message': 'Product created successfully!'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product.name = data.get('name', product.name)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price) 

            category_id = data.get('category_id')
            if category_id:
                category = get_object_or_404(ProductCategory, id=category_id)
                product.category = category
            
            if 'product_image' in data:
                product_image = data['product_image']  
                product.product_image = product_image
            
            product.save()
            return JsonResponse({'message': 'Product updated successfully!'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format!'}, status=400)

    return JsonResponse({
        'product_id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price, 
        'category_id': product.category.id,
        'product_image': product.product_image.url if product.product_image else None,
    })

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
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
