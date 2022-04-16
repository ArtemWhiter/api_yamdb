from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
