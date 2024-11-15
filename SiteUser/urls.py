from django.urls import path
from .views import (
    get_users_list, 
    create_site_user, 
    update_site_user, 
    delete_site_user,
    get_user_by_id,
    update_staff_user,
    update_customer_user,
    send_verification_code,
    verify_code,
    reset_password,
    login,
    admin_login,
    google_login,
    like_product,
    get_liked_products,
    get_addresses_list,
    update_address,
    delete_address,
    get_payment_methods_list,
    update_payment_method,
    delete_payment_method,
)

urlpatterns = [
    path('li-users/', get_users_list, name='get_users_list'),
    path('create/', create_site_user, name='create_site_user'),
    path('<int:id>/', get_user_by_id, name='get_user_by_id'),
    path('<int:id>/update/', update_site_user, name='update_site_user'),
    path('<int:id>/delete/', delete_site_user, name='delete_site_user'),
    path('profile/<int:id>/', get_user_by_id, name='get_staff_user_by_id'),
    path('staff/<int:id>/update/', update_staff_user, name='update_staff_user'),
    path('customer/<int:id>/update/', update_customer_user, name='update_customer_user'),
    


    # Các URL cho chức năng thích sản phẩm
    path('like-product/', like_product, name='like_product'),
    path('liked-products/<int:user_id>/', get_liked_products, name='get_liked_products'),

    # Các URL cho địa chỉ
    path('addresses/<int:user_id>/', get_addresses_list, name='get_addresses_list'),
    path('addresses/<int:user_id>/<int:address_id>/update/', update_address, name='update_address'),
    path('addresses/<int:user_id>/<int:address_id>/delete/', delete_address, name='delete_address'),

    # Các URL cho phương thức thanh toán
    path('payment-methods/<int:user_id>/', get_payment_methods_list, name='get_payment_methods_list'),
    path('payment-methods/<int:user_id>/<int:payment_method_id>/update/', update_payment_method, name='update_payment_method'),
    path('payment-methods/<int:user_id>/<int:payment_method_id>/delete/', delete_payment_method, name='delete_payment_method'),
]
