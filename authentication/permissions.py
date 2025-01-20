from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer') and request.user.customer is not None

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'supervisor') and request.user.supervisor is not None