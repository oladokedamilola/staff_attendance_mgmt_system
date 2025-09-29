from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from leave import views as notifications
urlpatterns = [
    path("admin/", admin.site.urls),

    # Project apps
    path("", include("core.urls")),          # Home, About, Contact
    path("accounts/", include("accounts.urls")),
    path("attendance/", include("attendance.urls")),
    path("leave/", include("leave.urls")),
    path("staff/", include("staff.urls")),
    path("adminpanel/", include("adminpanel.urls")),
    
    
    
    
    path('notifications/', notifications.notifications_list, name='notifications_list'),
    path('notifications/mark-read/<int:notification_id>/', notifications.mark_notification_read, name='notifications_mark_read'),
    path('notifications/mark-all-read/', notifications.mark_all_notifications_read, name='notifications_mark_all'),
]

# ✅ Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
