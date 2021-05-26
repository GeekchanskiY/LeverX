from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    def is_teacher(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or request.user.pk and request.user.status == "Teacher")