import sys
import getopt
import mail_tools

def print_help():
    print("Usage: your_script.py -h|--help -s|--server=<SMTP server> -r|--sender=<sender email> "
          "-f|--receivers=<receiver emails> -t|--subject=<subject> -a|--text=<message text> "
          "--attachment=<attachment path>")
    print("")
    print("Options:")
    print("-h, --help                   Show help message and exit")
    print("-s --server=<SMTP server>   SMTP server address")
    print("-p --port=<SMTP port>   SMTP port address")
    print("-sr, --sender=<sender email>  Sender email address")
    print("-r, --receivers=<receiver emails>   Comma-separated list of receiver email addresses")
    print("-j, --subject=<subject>      Subject of the email")
    print("-t, --text=<message text>    Body text of the email")
    print("-a, --attachment=<attachment path>   Path to the attachment file")
    print("")
    print("Example:")
    print("send_to_mail.py -s smtp.example.com -r sender@example.com -f receiver1@example.com,receiver2@example.com "
          "-t 'Test email' -a 'Hello, this is a test email.' --attachment /path/to/attachment.txt")

def get_arguments():
    global smtp_server
    global smtp_port
    global sender_email
    global receiver_emails
    global subject
    global message_text
    global attachment_path
    smtp_port = 25

    # define parameters
    short_options = "hs:sr:p:r:j:t:a:"
    long_options = ["help", "server=", "port=", "sender=", "receivers=", "subject=", "text=", "attachment="]

    # get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 5:
        print_help()
        sys.exit(2)

    # process command line parameters
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print_help()
        elif current_argument in ("-s", "--server"):
            smtp_server = current_value
            print("SMTP server:", smtp_server)
        elif current_argument in ("-p", "--port"):
            smtp_port = current_value
            print("SMTP port:", smtp_port)
        elif current_argument in ("-sr", "--sender"):
            sender_email = current_value
            print("Sender email:", sender_email)
        elif current_argument in ("-r", "--receivers"):
            receiver_emails = current_value.split(',')
            print("Receiver emails:", receiver_emails)
        elif current_argument in ("-j", "--subject"):
            subject = current_value
            print("Subject:", subject)
        elif current_argument in ("-t", "--text"):
            message_text = current_value
            print("Message text:", message_text)
        elif current_argument in ("--attachment"):
            attachment_path = current_value
            print("Attachment path:", attachment_path)

    # process remaining arguments
    for value in values:
        print("Extra arguments:", value)

def main():

    email_sender = mail_tools.EmailSender(smtp_server, smtp_port, sender_email)
    email_sender.send_email(receiver_emails, subject, message_text, attachment_path)

if __name__ == '__main__':
    get_arguments()
    main()