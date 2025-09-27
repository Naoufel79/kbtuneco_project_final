from .models import Message

def unread_messages(request):
    """Add unread message count to template context."""
    if request.user.is_authenticated:
        try:
            unread_count = request.user.profile.received_messages.filter(read=False).count()
            return {'unread_message_count': unread_count}
        except:
            return {'unread_message_count': 0}
    return {'unread_message_count': 0}
