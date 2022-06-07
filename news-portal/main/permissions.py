from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == obj.id or request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or obj.user_id == request.user)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user.is_superuser)
