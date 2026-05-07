import os
import zipfile
import smtplib
from email.mime.text import MIMEText
from celery import current_app, group, chord
from celery.utils.log import get_task_logger
from image import blur_image
from mail import send_email
from models import get_all_subscribers
from config import TEMP_FOLDER, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

logger = get_task_logger(__name__)

os.makedirs(TEMP_FOLDER, exist_ok=True)

@current_app.task(bind=True)
def process_single_image(self, src_path: str, dst_path: str):
    try:
        blur_image(src_path, dst_path)
        return dst_path
    except Exception as e:
        raise self.retry(exc=e, countdown=5)

@current_app.task
def make_archive_and_send_email(image_paths, user_email, order_id):
    archive_name = f'blurred_{order_id}.zip'
    archive_path = os.path.join(TEMP_FOLDER, archive_name)
    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for img_path in image_paths:
            if os.path.exists(img_path):
                zipf.write(img_path, arcname=os.path.basename(img_path))
                os.remove(img_path)
    send_email(order_id, user_email, archive_path)
    os.remove(archive_path)
    return f'Finished for order {order_id}'

def send_info_email(receiver: str):
    msg = MIMEText('Еженедельная рассылка о сервисе обработки изображений.')
    msg['Subject'] = 'Еженедельная рассылка'
    msg['From'] = SMTP_USER
    msg['To'] = receiver
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, receiver, msg.as_string())

@current_app.task
def send_weekly_newsletter():
    emails = get_all_subscribers()
    for email in emails:
        send_info_email(email)
    return f'Newsletter sent to {len(emails)} subscribers''