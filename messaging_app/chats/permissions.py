from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow owners to access their own messages or conversations
        return obj.user == request.user
