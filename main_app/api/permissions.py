from rest_framework import permissions

class IsAuthorOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return request.user.group

class IsMainUser(permissions.IsAuthenticated):
    def has_permission(self, request, view, obj):
        return request.user.group
    
    def has_object_permission(self, request, view, obj):
        return request.user.group