from rest_framework import permissions
from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj should be a Message or Conversation with a `.conversation` attribute
        conversation = getattr(obj, 'conversation', None)
        if conversation:
            return request.user in conversation.participants.all()
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow owners to access their own messages or conversations
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to perform any action
    on messages (view, create, update, delete).
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For PUT, PATCH, DELETE, GET — ensure user is participant of the conversation
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            conversation = getattr(obj, 'conversation', None)
            if conversation:
                return request.user in conversation.participants.all()
        return False
