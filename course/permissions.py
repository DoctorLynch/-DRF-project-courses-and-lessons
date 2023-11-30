from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == view.obj.owner


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False
