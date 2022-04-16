from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
            if request.user.is_authenticated:
                return request.user.role == "admin"
            else:
                return request.method in SAFE_METHODS
