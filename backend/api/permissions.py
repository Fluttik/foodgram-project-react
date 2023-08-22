from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

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
