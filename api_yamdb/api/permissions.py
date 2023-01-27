from rest_framework import permissions


class ObjectReadOnly(permissions.BasePermission):
    """Базовый пермишен, разрешает только безопасные запросы к объектам.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user, request.method in permissions.SAFE_METHODS


class AdminOnly(ObjectReadOnly):
    """Разрешает доступ к списку и объекту только пользователям с ролью admin.
    """
    def has_permission(self, request, view):
        return self.user.is_authenticated and self.user.is_admin

    def has_object_permission(self, request, view, obj):
        return self.user.is_authenticated and self.user.is_admin
