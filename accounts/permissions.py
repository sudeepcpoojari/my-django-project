from rest_framework.permissions import BasePermission

class IsTeacherOrPrincipal(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['teacher','principal']


class IsPrincipal(BasePermission):
   def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.role in ['principal']
