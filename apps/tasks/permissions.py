from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user

    # BasePermission — базовый класс для создания собственных разрешений DRF.
    # SAFE_METHODS — безопасные методы: GET, HEAD, OPTIONS.
    # has_object_permission() — проверяет разрешение для конкретного объекта.
    # obj.owner == request.user — проверяет, совпадает ли владелец объекта с текущим пользователем.