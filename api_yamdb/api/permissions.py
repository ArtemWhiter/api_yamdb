from urllib import request
from rest_framework import permissions

class NewUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user


class IsAdminOnly(permissions.BasePermission):

    #def has_permission(self, request, view):
        #return bool(request.user and request.user.is_staff)
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_staff
            #or user.is_superuser
        )

    #def has_object_permission(self, request, view, obj):
       # user = request.user
        #return (
            #user.is_authenticated and user.is_admin
            #or user.is_superuser
        #)    


class IsUserOrAdminOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
