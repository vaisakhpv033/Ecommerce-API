from rest_framework import serializers
from .models import Cart
from products.models import Products

class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model.
    Provides product details within the cart
    """

    product_title = serializers.CharField(source="product.product_title", read_only=True)
    product_subtitle = serializers.CharField(source="product.product_subtitle", read_only=True)
    product_image = serializers.URLField(source="product.image", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_title",
            "product_price",
            "product_image",
            "product_subtitle",
            "quantity",
            "created_at",
            "updated_at",
        ]

    def validate_product(self, value):
        """
        Ensure a product exist and is not already in the cart
        """

        # check if the product exists and is available
        if not Products.objects.filter(
            id=value.id, is_available=True, stock__gt=0
        ).exists():
            raise serializers.ValidationError(
                "This product is not available for purchase."
            )

        user = self.context["request"].user

        # check if the product is already in the cart
        if Cart.objects.filter(user=user, product=value).exists():
            raise serializers.ValidationError("This product is already in your cart.")

        return value
    
    def validate_quantity(self, value):
        """
        Ensure the quantity is a positive integer and does not exceed available stock
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        
        if value > 5:
            raise serializers.ValidationError("You cannot add more than 5 items of the same product to the cart.")

        product = self.initial_data.get("product")
        if product and product.stock < value:
            raise serializers.ValidationError(
                "Requested quantity exceeds available stock."
            )

        return value
