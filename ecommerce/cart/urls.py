from rest_framework.routers import DefaultRouter

from .views import CartViewSet, AddressesViewSet

router = DefaultRouter()
router.register("cart", CartViewSet, basename='cart')
router.register("address", AddressesViewSet, basename='address')



urlpatterns = router.urls