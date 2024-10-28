from django.urls import path
from .views import (
    banner_list,
    create_banner,
    get_banner_by_id,
    update_banner,
    update_banner_status,
    delete_banner,
)

urlpatterns = [
    path('', banner_list, name='banner_list'),  
    path('create/', create_banner, name='create_banner'), 
    path('<int:banner_id>/', get_banner_by_id, name='get_banner_by_id'),  
    path('<int:banner_id>/update/', update_banner, name='update_banner'),  
    path('<int:banner_id>/status/', update_banner_status, name='update_banner_status'), 
    path('<int:banner_id>/delete/', delete_banner, name='delete_banner'), 
]