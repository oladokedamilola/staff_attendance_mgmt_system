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

from django.contrib.auth import views as auth_views

urlpatterns += [
    path("password-reset/", 
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="password_reset"),
    path("password-reset/done/", 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name="password_reset_complete"),
]

# ✅ Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
