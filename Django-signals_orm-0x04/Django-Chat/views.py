from .models import Message
from .utils import build_thread  # Only if you placed the helper in utils.py

def get_conversation_threads():
    threads = []
    top_level_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies__sender', 'replies__receiver')

    for msg in top_level_messages:
        threads.append(build_thread(msg))

    return threads
