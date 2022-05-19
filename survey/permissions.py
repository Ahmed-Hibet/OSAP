from rest_framework import permissions

class IsRespondent(permissions.BasePermission):
    # message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.roll.roll_name == 'Respondent'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.roll.roll_name == 'Admin'