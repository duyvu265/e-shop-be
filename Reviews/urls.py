from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/', views.get_reviews_by_product, name='get_reviews_by_product'),
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('<int:review_id>/update/', views.update_review, name='update_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
]
