import smtplib
from email.mime.text import MIMEText
from email.header import Header

EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_SENDER = 'noreply@example.com'

def send_mail(recipients, subject, body, sender=EMAIL_SENDER):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    s = smtplib.SMTP(EMAIL_HOST, 587, timeout=10)
    try:
        s.starttls()
        s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        s.sendmail(msg['From'], recipients, msg.as_string())
    finally:
        s.quit()
