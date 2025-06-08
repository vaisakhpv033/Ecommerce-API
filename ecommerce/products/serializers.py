from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'product_title', 'product_subtitle', 'description', 'price', 
            'stock', 'image', 'is_available', 'created_at', 'updated_at'
            ]
        read_only_fields = ['id']

