# leave/utils.py
import logging
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()

def send_leave_notification(sender, recipient, subject, message, request=None):
    """
    Sends an email and creates an on-site notification safely.

    Args:
        sender (User): The user who triggered the notification.
        recipient (User or list/queryset of Users): Recipient(s) of the notification.
        subject (str): Subject for email/notification.
        message (str): Message content.
        request (HttpRequest, optional): Only used for internal logging; no flash messages shown.
    """
    # Ensure recipient is a list
    if not isinstance(recipient, (list, tuple, models.QuerySet)):
        recipient = [recipient]

    for user in recipient:
        if not isinstance(user, User):
            logger.warning(f"Invalid recipient type: {type(user)}")
            continue

        # Save notification in DB
        try:
            Notification.objects.create(
                sender=sender,
                recipient=user,
                subject=subject,
                message=message
            )
        except IntegrityError as e:
            logger.error(f"Failed to create notification for {user}: {e}")
            continue
        except Exception as e:
            logger.exception(f"Unexpected error creating notification for {user}: {e}")
            continue

    # Send email
    emails = [user.email for user in recipient if getattr(user, "email", None)]
    if emails:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=emails,
                fail_silently=False,
            )
        except BadHeaderError as e:
            logger.error(f"Bad header in email: {e}")
        except Exception as e:
            logger.exception(f"Failed to send email to {emails}: {e}")

    # Remove on-site flash messages to keep UI professional
    # Notifications are still saved and emails sent silently
