from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out first
    user.delete()    # Trigger post_delete signal
    return redirect('home')  # Replace with your home or login page

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

# Recursive function to build a threaded structure
def build_thread(message):
    return {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'content': message.content,
        'timestamp': message.timestamp,
        'replies': [build_thread(reply) for reply in message.replies.all()]
    }

@login_required
def user_messages_view(request):
    user = request.user

    # Fetch top-level messages either sent or received by the current user
    top_level_messages = (
        Message.objects.filter(parent_message__isnull=True)
        .filter(sender=user) | Message.objects.filter(receiver=user)
    ).select_related('sender', 'receiver')\
     .prefetch_related('replies__sender', 'replies__receiver')\
     .distinct()

    # Build threaded message structure
    message_threads = [build_thread(msg) for msg in top_level_messages]

    return render(request, 'messaging/threaded_messages.html', {
        'message_threads': message_threads
    })
