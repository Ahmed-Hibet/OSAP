from rest_framework import permissions

class IsRespondent(permissions.BasePermission):
    # message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.roll.roll_name == 'Respondent'