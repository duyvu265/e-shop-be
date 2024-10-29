from django.urls import path
from .views import category_list

urlpatterns = [
    path('', category_list, name='category-list'),
    # path('', category_create, name='category-create'),
    # path('<int:pk>/', category_detail, name='category-detail'),
    # path('<int:pk>/update/', category_update, name='category-update'),
    # path('<int:pk>/delete/', category_delete, name='category-delete'),
]
