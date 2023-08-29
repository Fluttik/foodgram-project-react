from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Данный класс используется для доступа к данным.
    если пользователь авторизован то ему доступны изменения данных
    автором которых он является
    если пользователь не авторизован - доступ только к SAFE методам"""

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
