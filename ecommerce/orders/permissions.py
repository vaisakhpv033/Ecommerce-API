from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnlyForOwner(BasePermission):
    """
    - Admin: full access
    - Authenticated user: only view own orders
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.method in SAFE_METHODS and obj.user == request.user
    

