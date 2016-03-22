# coding=utf-8

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from . import emails


def send_email(email, subject, message):
    """Send email."""
    send_mail(
        subject=subject, message=message, html_message=message,
        recipient_list=[email], from_email=settings.DEFAULT_FROM_EMAIL
    )


def send_confirmation_email(confirmation):
    """Send confirmation email."""
    message = render_to_string(
        emails.VERIFICATION['template'], {'code': confirmation.code}
    )
    send_email(
        subject=emails.VERIFICATION['subject'], message=message,
        email=confirmation.user.email
    )


def send_restore_password_email(confirmation):
    """Send email with instructions for restore password."""
    message = render_to_string(
        emails.RESTORE_PASSWORD['template'], {'code': confirmation.code}
    )
    send_email(
        subject=emails.RESTORE_PASSWORD['subject'], message=message,
        email=confirmation.user.email
    )
