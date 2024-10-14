"""
URL configuration for e_shop_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Products.views import (
    product_list,
    create_product,
    update_product,
    delete_product,
    get_product_by_id
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='products list'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    
]
