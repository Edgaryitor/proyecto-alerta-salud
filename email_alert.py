from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pytz

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email_alert(user_email, user_password, recipient_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = user_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Conexión al servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Iniciar conexión segura
            server.login(user_email, user_password)
            server.send_message(msg)
            print("Correo electrónico enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
