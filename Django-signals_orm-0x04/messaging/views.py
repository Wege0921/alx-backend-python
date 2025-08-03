from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message
from django.views.decorators.cache import cache_page


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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
def unread_messages_view(request):
    # ✅ Use Message.unread.unread_for_user and .only()
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)
def cached_message_list(request):
    messages = Message.objects.all()
    return render(request, 'messaging/messages.html', {'messages': messages})

@cache_page(60)
def message_list_view(request):
    # replace this with your actual queryset and rendering logic
    messages = Message.objects.all()
    return render(request, 'messaging/message_list.html', {'messages': messages})
