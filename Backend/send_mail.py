from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import dotenv

dotenv.load_dotenv()

def send_email(to_email: str, subject: str, body: str):
    try:
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) # Establishing server/connecting to the Gmail server
        server.starttls()
        server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))

        msg = MIMEMultipart()
        msg["From"] = os.getenv('SENDER_EMAIL')
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server.sendmail(os.getenv('SENDER_EMAIL'), to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

def send_email_to_you(data):
    admin_subject = f"New Contact Request from {data.name}"
    admin_body = f"Name: {data.name}\nEmail: {data.email}\nMessage: {data.message}"
    send_email(os.getenv('SENDER_EMAIL'), admin_subject, admin_body)


def send_email_to_user(data):
    user_subject = "Your Contact Request Has Been Received"
    user_body = f"Dear {data.name},\n\nThank you for reaching out! We have received your message and will get back to you soon.\n\nYour Message:\n{data.message}\n\nBest Regards,\nEatWise."
    send_email(data.email, user_subject, user_body)