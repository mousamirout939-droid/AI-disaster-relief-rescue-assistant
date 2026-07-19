"""SMTP email sending (OTP, report confirmations, emergency alerts)."""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import settings
from config.logging import logger


class EmailService:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.sender = settings.EMAIL_FROM

    def send_email(self, to: str, subject: str, html_body: str) -> bool:
        if not self.host:
            logger.warning("SMTP not configured — skipping email to %s (%s)", to, subject)
            return False

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = to
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.sender, [to], msg.as_string())
            return True
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to send email to %s: %s", to, exc)
            return False
