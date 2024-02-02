from rest_framework.permissions import BasePermission

from users.models import User


class IsUserOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == User.Role.OWNER)
