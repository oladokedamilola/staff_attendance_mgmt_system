# leave/context_processors.py
from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        # Full queryset first
        notifications_qs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
        
        # Count unread before slicing
        unread_count = notifications_qs.filter(is_read=False).count()
        
        # Slice only for recent notifications
        notifications = notifications_qs[:10]
        
        return {
            "notifications_list": notifications,
            "unread_notifications_count": unread_count
        }
    return {}
