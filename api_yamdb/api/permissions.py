from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права администратора или только чтение."""

    message = 'Недостаточно прав, вы не администртор!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.is_admin)
                    )
                )
