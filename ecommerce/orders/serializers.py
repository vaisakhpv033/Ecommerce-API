from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_title',
            'product_subtitle',
            'quantity',
            'price',
            'status',
        ]
        read_only_fields = fields 

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'order_number',
            'total',
            'status',
            'created_at',
            'updated_at',
            'items',
        ]
        read_only_fields = [
            'id',
            'user',
            'order_number',
            'total',
            'created_at',
            'updated_at',
            'items',
        ]


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'status'
        ]