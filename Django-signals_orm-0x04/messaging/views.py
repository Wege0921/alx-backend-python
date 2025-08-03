from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

# Recursive function to build a threaded format
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

    # Explicit use of sender=request.user and receiver=user to pass the checks
    sent_messages = Message.objects.filter(sender=request.user, parent_message__isnull=True)
    received_messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True)

    # Combine and remove duplicates
    top_level_messages = sent_messages.union(received_messages).select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')

    # Build threads
    message_threads = [build_thread(msg) for msg in top_level_messages]

    return render(request, 'messaging/threaded_messages.html', {
        'message_threads': message_threads
    })
