# src/notification/notifier.py

import smtplib
from email.mime.text import MIMEText
from config import Config

class Notifier:
    def __init__(self):
        self.email = Config.NOTIFICATION_EMAIL

    def send_notifications(self, report):
        msg = MIMEText(report)
        msg['Subject'] = "GitHub Sentinel Report"
        msg['From'] = "sentinel@example.com"
        msg['To'] = self.email

        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
