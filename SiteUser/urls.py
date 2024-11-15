from django.urls import path
from .views import (
    get_users_list, 
    create_site_user, 
    update_site_user, 
    delete_site_user,
    get_user_by_id,
    update_staff_user,
    update_customer_user
    
)

urlpatterns = [
    path('li-users', get_users_list, name='get_users_list'),
    path('create/', create_site_user, name='create_site_user'),
    path('<int:id>', get_user_by_id, name='get_user_by_id'),
    path('<int:id>/update/', update_site_user, name='update_site_user'),
    path('<int:id>/update/', update_site_user, name='update_site_user'),
    path('<int:id>/delete/', delete_site_user, name='delete_site_user'),
    path('profile/<int:id>/', get_user_by_id, name='get_staff_user_by_id'),
    path('staff/<int:id>/update/', update_staff_user, name='update_staff_user'),
    path('customer/<int:id>/update/', update_customer_user, name='update_customer_user'),
]
