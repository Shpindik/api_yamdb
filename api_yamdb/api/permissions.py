from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Проверяет, является ли пользователь администратором.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Позволяет доступ только администраторам или предоставляет доступ
    только для чтения.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объекты только авторам,
    модераторам и администраторам.
    Разрешения только для чтения разрешены для любого запроса.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)
