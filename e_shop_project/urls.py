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
from django.urls import path,include
from SiteUser.views import login,create_site_user,google_login,admin_login
from Banner.views import banner_list
from ProductsCategory.views import category_list
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name="login"),
    path('google-login/', google_login, name='google_login'),
    path('register/', create_site_user ,name="register"),
    path('products/', include('Products.urls')), 
    path('v1/admin/login/', admin_login,name='admin_login'), 
    path('li-banners/', banner_list, name='banner_list'), 
    path('categories/', category_list), 
    path('user/', include('SiteUser.urls')), 
    path('cart/', include('ShoppingCart.urls')), 
    path('banners/', include('Banner.urls')), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    
]
