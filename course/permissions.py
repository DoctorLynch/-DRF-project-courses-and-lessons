from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and (view.action != 'destroy' or view.action != 'create')


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner and (view.action == 'list' or view.action == 'update')
