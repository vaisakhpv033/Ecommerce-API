from django.urls import path
from .views import CreateOrderView, OrderViewSet, OrderItemListView, OrderItemUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", OrderViewSet, basename='orders')

urlpatterns = router.urls + [
    path('checkout/', CreateOrderView.as_view(), name='checkout'),
    path("order-items/", OrderItemListView.as_view(), name="orderitem-list"),
    path("order-items/<int:pk>/", OrderItemUpdateView.as_view(), name="orderitem-update"),
]
