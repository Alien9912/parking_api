"""
В этом файле будут секретные данные

Для создания почтового сервиса воспользуйтесь следующими инструкциями

- Yandex: https://yandex.ru/support/mail/mail-clients/others.html
- Google: https://support.google.com/mail/answer/7126229?visit_id=638290915972666565-928115075
"""

# https://yandex.ru/support/mail/mail-clients/others.html

import os

SMTP_USER = "ПОЧТА ОТПРАВИТЕЛЯ"
SMTP_HOST = "smtp.yandex.com"
SMTP_PASSWORD = "ПАРОЛЬ ОТ ПОЧТЫ ОТПРАВИТЕЛЯ / СПЕЦИАЛЬНЫЙ ТОКЕН ПРИЛОЖЕНИЯ"
SMTP_PORT = 587

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
UPLOAD_FOLDER = "uploads"
TEMP_FOLDER = "temp"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}}