from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(user_email, booking_id, amount):
    subject = "Booking and Payment confirmation"
    message = (
        f"Your booking {booking_id} has been confirmed.\n"
        f"Amount received: ${amount}.\n\nThank you for choosing ALX Travel"
    )
    send_mail(
        subject, message, settings.EMAIL_HOST_USER,
        recipient_list=[user_email], fail_silently=False
    )

@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    subject = "Booking confirmation"
    message = (
        f"Hello!\n\nYour booking was successful.\n\n"
        f"Details:\n\n{booking_details}"
    )
    send_mail(
        subject, message, settings.EMAIL_HOST_USER,
        recipient_list=[user_email], fail_silently=False
    )

    return f"Booking confirmation email sent to {user_email}"
