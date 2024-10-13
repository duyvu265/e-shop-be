from django.urls import path
from .views import (
    site_user_list, create_site_user, update_site_user, delete_site_user,
)

urlpatterns = [
    path('users/', site_user_list, name='site_user_list'),
    path('users/create/', create_site_user, name='create_site_user'),
    path('users/<int:id>/update/', update_site_user, name='update_site_user'),
    path('users/<int:id>/delete/', delete_site_user, name='delete_site_user'),
]
