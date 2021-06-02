import csv
import io

from django.conf import settings
from django.core.mail import EmailMessage

from .models import URL


def send_email(emails, subject, message):
    email = EmailMessage(
        subject,
        message,
        [settings.DEFAULT_FROM_EMAIL],
        emails,
        [],
    )
    return email.send(fail_silently=False)


def make_url_dump(user_id, user_username, user_email):
    urls = URL.objects.filter(owner_id=user_id)
    header = ['name', 'original_url', 'short_url']
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(header)
    for u in urls:
        writer.writerow(
            [
                u.name,
                u.original_url,
                u.short_url,
            ]
        )

    email = EmailMessage(
        subject=f'{user_username} urls dump',
        from_email=[settings.DEFAULT_FROM_EMAIL],
        to=[user_email],
        bcc=[],
    )
    f.seek(0)
    email.attach(f'{user_username} urls dump', f.read())
    email.send(fail_silently=False)
    f.close()
    return None
