from rest_framework import permissions

class IsAuthorOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return request.user.group is not None

class IsMainUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.group is not None
    
    def has_object_permission(self, request, view, obj):
        return request.user.group is not None