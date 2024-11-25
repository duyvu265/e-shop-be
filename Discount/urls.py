from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_discounts, name='list_discounts'),
    path('create/', views.create_discount, name='create_discount'),
    path('<int:pk>/', views.get_discount, name='get_discount'),
    path('<int:pk>/update/', views.update_discount, name='update_discount'),
    path('<int:pk>/delete/', views.delete_discount, name='delete_discount'),
]
