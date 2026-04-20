from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_reservation_confirmation(reservation):
    subject = f'Reservation Confirmed — Haruki, {reservation.date.strftime("%d %B %Y")}'

    message = render_to_string('restaurant/emails/reservation_confirmation.txt', {
        'reservation': reservation,
    })

    send_mail(
        subject      = subject,
        message      = message,
        from_email   = 'Haruki Restaurant <reservations@haruki-bkk.com>',
        recipient_list = [reservation.email],
        fail_silently = True,   # won't crash the site if email fails
    )


def send_reservation_update(reservation):
    subject = f'Reservation Update — Haruki #{reservation.pk}'

    message = render_to_string('restaurant/emails/reservation_update.txt', {
        'reservation': reservation,
    })

    send_mail(
        subject        = subject,
        message        = message,
        from_email     = 'Haruki Restaurant <reservations@haruki-bkk.com>',
        recipient_list = [reservation.email],
        fail_silently  = True,
    )