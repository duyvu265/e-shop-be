from django.urls import path
from Products.views import (
    product_list,
    create_product,
    update_product,
    delete_product,
    get_product_by_id
)

urlpatterns = [
    path('products/', product_list, name='products list'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    
]
