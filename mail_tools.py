import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class EmailSender:
    """
    A class for sending emails with attachments using SMTP.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.
        sender_email (str): The email address of the sender.

    Methods:
        send_email: Sends an email with attachments to one or more recipients.
    """

    def __init__(self, smtp_server, smtp_port, sender_email):
        """
        Initializes the EmailSender object.

        Args:
            smtp_server (str): The SMTP server address.
            smtp_port (int): The SMTP server port.
            sender_email (str): The email address of the sender.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email

    def send_email(self, receiver_emails, subject, message_text, attachment_path=None):
        """
        Sends an email with attachments to one or more recipients.

        Args:
            receiver_emails (list): A list of email addresses of the recipients.
            subject (str): The subject of the email.
            message_text (str): The body text of the email.
            attachment_path (str, optional): The path to the attachment file.

        Returns:
            None.
        """
        # Create a MIMEMultipart object for formatting the message
        message = MIMEMultipart()

        # Add the text part of the email
        message.attach(MIMEText(message_text))

        if attachment_path:
            # Create a MIMEApplication object for the attached file
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read())

            # Set the Content-Disposition header for the attachment
            filename = os.path.basename(attachment_path)
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)

            # Add the attachment to the message
            message.attach(attachment)

        # Set the necessary headers of the email
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = ', '.join(receiver_emails)

        try:
            # Establish a connection with the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)

            # Send the email
            server.sendmail(self.sender_email, receiver_emails, message.as_string())

            # Close the connection
            server.quit()

            print('Email successfully sent.')
        except smtplib.SMTPException as e:
            print(f'Error while sending email: {str(e)}')


if __name__ == '__main__':
    # Example usage of the EmailSender class
    smtp_server = 'eurasia-kz.mail.protection.outlook.com'
    smtp_port = 25
    sender_email = 'vladimir.muzychenko@eurasia.kz'
    receiver_emails = ['receiver1@example.com', 'receiver2@example.com', 'receiver3@example.com']
    subject = 'Test email with attachment'
    message_text = 'Hello, this is a test email.'
    attachment_path = 'data.xlsx'

    # Create an instance of the EmailSender class
    email_sender = EmailSender(smtp_server, smtp_port, sender_email)

    # Send the email
    email_sender.send_email(receiver_emails, subject, message_text, attachment_path)
