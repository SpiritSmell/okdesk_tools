import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText


def send_email(sender_email, sender_password, receiver_email, subject, message, file_path):
    # Создаем объект MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Добавляем текстовое сообщение
    msg.attach(MIMEText(message, 'plain'))

    # Открываем файл в режиме бинарного чтения
    with open(file_path, 'rb') as attachment:
        # Создаем объект MIMEBase
        part = MIMEBase('application', 'octet-stream')
        # Устанавливаем данные файла
        part.set_payload(attachment.read())
        # Кодируем вложение в Base64
        encoders.encode_base64(part)
        # Устанавливаем заголовок файла
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        # Прикрепляем вложение к сообщению
        # msg.attach(part)

    # Устанавливаем SMTP-сервер и порт
    smtp_server = 'eurasia-kz.mail.protection.outlook.com'
    smtp_port = 25

    # Инициализируем SMTP-сессию
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Начинаем защищенное соединение
        server.login(sender_email)  # Входим в аккаунт отправителя
        server.send_message(msg)  # Отправляем сообщение

# Пример использования
sender_email = 'okdesk_reports@eurasia.kz'
sender_password = 'your_password'
receiver_email = 'recipient@example.com'
subject = 'Пример отправки файла по электронной почте'
message = 'Привет, вот файл, который я хотел отправить.'
file_path = 'path/to/file.pdf'

send_email(sender_email, sender_password, receiver_email, subject, message, file_path)
