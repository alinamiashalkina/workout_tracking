from rest_framework.permissions import BasePermission


class IsAdminOrTrainerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or
                request.user.is_trainer
        )

    def has_object_permission(self, request, view, obj):
        return obj.trainer == request.user or request.user.is_admin


class IsAdminOrClientPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or
                request.user.is_client
        )

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user or request.user.is_admin


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
