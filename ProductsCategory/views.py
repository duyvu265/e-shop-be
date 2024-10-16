from django.http import JsonResponse
from .models import ProductCategory

def category_list(request):
    if request.method == 'GET':
        categories = ProductCategory.objects.prefetch_related('subcategories').all()

        category_list = []
        for category in categories:
            subcategories = [
                {
                    'id': subcategory.id,
                    'category_name': subcategory.category_name,
                    'image_url': subcategory.image_url  
                }
                for subcategory in category.subcategories.all()
            ]

            category_data = {
                'id': category.id,
                'category_name': category.category_name,
                'image_url': category.image_url,  
                'parent_category': {
                    'id': category.parent_category.id,
                    'category_name': category.parent_category.category_name,
                    'image_url': category.parent_category.image_url  
                } if category.parent_category else None,
                'subcategories': subcategories
            }

            category_list.append(category_data)

        return JsonResponse(category_list, safe=False)

    return JsonResponse({'error': 'Invalid request method!'}, status=400)