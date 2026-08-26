from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение: автор может редактировать/удалять свой контент,
    остальные только читают.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для остальных методов проверяем, что пользователь - автор
        return obj.author == request.user


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Разрешение: автор или администратор могут редактировать/удалять
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff