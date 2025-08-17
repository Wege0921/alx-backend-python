def build_thread(message):
    thread = {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'content': message.content,
        'timestamp': message.timestamp,
        'replies': []
    }
    for reply in message.replies.all():
        thread['replies'].append(build_thread(reply))
    return thread
