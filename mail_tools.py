import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email

    def send_email(self, receiver_emails, subject, message_text, attachment_path=None):
        # Создаем объект MIMEMultipart для форматирования сообщения
        message = MIMEMultipart()

        # Добавляем текстовую часть письма
        message.attach(MIMEText(message_text))

        if attachment_path:
            # Создаем объект MIMEApplication для вложенного файла
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read())

            # Задаем заголовок Content-Disposition для вложения
            filename = os.path.basename(attachment_path)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)

            # Добавляем вложение к сообщению
            message.attach(attachment)

        # Заполняем необходимые заголовки письма
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = ', '.join(receiver_emails)

        try:
            # Устанавливаем соединение с SMTP сервером
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)

            # Отправляем письмо
            server.sendmail(self.sender_email, receiver_emails, message.as_string())

            # Закрываем соединение
            server.quit()

            print('Письмо успешно отправлено.')
        except smtplib.SMTPException as e:
            print(f'Ошибка при отправке письма: {str(e)}')


if __name__ == '__main__':
    # Пример использования класса EmailSender
    smtp_server = 'eurasia-kz.mail.protection.outlook.com'
    smtp_port = 25
    sender_email = 'vladimir.muzychenko@eurasia.kz'
    receiver_emails = ['receiver1@example.com', 'receiver2@example.com', 'receiver3@example.com']
    subject = 'Тестовое письмо с вложением'
    message_text = 'Привет, это тестовое письмо.'
    attachment_path = 'data.xlsx'

    # Создаем экземпляр класса EmailSender
    email_sender = EmailSender(smtp_server, smtp_port, sender_email)

    # Отправляем письмо
    email_sender.send_email(receiver_emails, subject, message_text, attachment_path)
