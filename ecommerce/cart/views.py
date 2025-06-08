from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart
from .serializers import CartSerializer

# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    """
    API for managing user carts
    """

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get the authenticated user's cart items
        """
        return Cart.objects.select_related("product").filter(
            user=self.request.user, product__is_available=True, product__stock__gt=0
        )

    def perform_create(self, serializer):
        """
        Add a product to the user's cart
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Hard delete a product from the cart
        """
        try:
            cart_item = self.get_object()
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Product not found in your cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear_cart(self, request):
        """
        Clear all products from the users cart
        """

        if not Cart.objects.filter(user=request.user).exists():
            return Response(
                {"message": "Your cart is already empty."},
                status=status.HTTP_404_NOT_FOUND,
            )

        Cart.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Cart cleared successfully."}, status=status.HTTP_204_NO_CONTENT
        )
