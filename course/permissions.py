from rest_framework.permissions import BasePermission


class IsOwnerOrIsSuperuserOrIsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_staff and (view.action != 'destroy' or view.action != 'create'):
            return True
        return request.user == view.get_object().owner and (view.action == 'list' or view.action == 'update')


class IsStaffOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner


class IsSuperuserOrIsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user == view.get_object().owner


class NotStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
        else:
            return True
