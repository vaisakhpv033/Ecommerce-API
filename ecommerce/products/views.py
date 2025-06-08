from rest_framework import viewsets, filters
from .models import Products
from .serializers import ProductSerializer
from .permissions import IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    
    This viewset provides CRUD operations for the Products model.
    """
    
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['product_title', 'product_subtitle']
    ordering_fields = ['created_at', 'price']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """
        Save the new product instance
        
        Args:
            serializer (Serializer): The serializer instance containing validated data.
        """
        serializer.save()