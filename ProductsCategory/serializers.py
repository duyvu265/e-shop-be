from rest_framework import serializers
from ProductsCategory.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True, required=False)  

    class Meta:
        model = ProductCategory
        fields = ['id', 'category_name', 'parent_category', 'subcategories']  
