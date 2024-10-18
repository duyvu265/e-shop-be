from django.urls import path
from .views import add_to_cart, update_cart_item, remove_from_cart,get_cart_items

urlpatterns = [
    path('get/', get_cart_items, name='get_cart_items'),  
    path('add/', add_to_cart, name='add_to_cart'),
    path('cart/item/<int:item_id>/update/', update_cart_item, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', remove_from_cart, name='remove_from_cart'),
]
