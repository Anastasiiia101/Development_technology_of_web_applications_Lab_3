from celery.decorators import task
from celery.utils.log import get_task_logger

from .utils import make_url_dump, send_email

logger = get_task_logger(__name__)


@task(name="send_url_dump", queue="url_dump")
def send_url_dump(user_id, user_username, user_email):
    logger.info("Creating url dump")
    return make_url_dump(user_id, user_username, user_email)


@task(name="send_emails_task", queue="email")
def send_emails_task(emails, subject, message):
    logger.info("Sent emails")
    return send_email(emails, subject, message)
