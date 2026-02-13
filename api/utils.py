import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings 
# send email using smtp
def sendEmail(email: str, message: str, subject: str ='Your verification code'):
    try:
        with smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(user = settings.EMAIL_HOST_USER, password= settings.EMAIL_HOST_PASSWORD)
            msg =  MIMEMultipart()
            msg["from"] = settings.EMAIL_HOST_USER
            msg["to"] = email
            msg["subject"] = subject
            msg.attach(MIMEText(message,'plain'))
            server.send_message(msg)        
    except Exception as e:
        pass
    