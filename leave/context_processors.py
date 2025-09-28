# leave/context_processors.py
from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]
        unread_count = notifications.filter(is_read=False).count()
        return {
            "notifications_list": notifications,
            "unread_notifications_count": unread_count
        }
    return {}
