from rest_framework.permissions import BasePermission, SAFE_METHODS

# Custom permission class to check whether user making request is same as current login user.
class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user