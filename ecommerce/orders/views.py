from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from cart.models import Addresses, Cart
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemUpdateSerializer, OrderItemSerializer
from .permissions import IsAdminOrReadOnlyForOwner

# Create your views here.
class CreateOrderView(APIView):
    """
    View to create an order from the user's cart.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        address_id = request.data.get("address_id")


        # validate address_id
        try:
            address = Addresses.objects.get(id=address_id, user=user)
        except Addresses.DoesNotExist:
            return Response(
                {"error": "Invalid address ID."},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        cart_items = Cart.objects.select_related("product").filter(user=user)
        if not cart_items.exists():
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"{item.product.product_title} has only {item.product.stock} items in stock."},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
        # calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # create order
        order = Order.objects.create(
            user=user, 
            total=total_price, 
            address=address.full_address, 
            phone_number=address.phone_number,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code
        )

        # create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_title=item.product.product_title,
                product_subtitle=item.product.product_subtitle,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

        # clear cart 
        cart_items.delete()

        return Response(
            {
                "message": "Order created successfully.",
                "order_id": order.id,
                "total_price": total_price,
                "order_number": order.order_number
            },
            status=status.HTTP_201_CREATED
        )



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnlyForOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """
        Save the order with the user as the creator.
        """
        return Response({"error": "Creating orders is not allowed through this endpoint."}, status=403)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "You are not allowed to update orders."}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response({"error": "Deleting orders is not allowed."}, status=403)
    


class OrderItemListView(ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]

class OrderItemUpdateView(UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer
    permission_classes = [IsAdminUser]