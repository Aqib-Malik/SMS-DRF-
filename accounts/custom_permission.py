from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'
    
class IsTeacherUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'teacher'
    
    
class IsAdminOrTeacherUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.user_type == 'admin' or request.user.user_type == 'teacher')
        )
