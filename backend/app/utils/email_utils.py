import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import get_settings

logger = logging.getLogger(__name__)

def send_reset_email(to_email: str, reset_link: str):
    # BUG-4 FIX: Read SMTP config from settings instead of hardcoded placeholders
    settings = get_settings()
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD

    if not smtp_user or not smtp_password or smtp_server == "smtp.example.com":
        logger.warning(
            "SMTP is not configured. Set SMTP_SERVER, SMTP_USER, SMTP_PASSWORD in .env "
            f"to enable password reset emails. Reset link for {to_email}: {reset_link}"
        )
        return  # Fail gracefully instead of crashing

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = "Password Reset Request"
        body = f"Click the link to reset your password: {reset_link}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
    except Exception as e:
        logger.error(f"Failed to send reset email to {to_email}: {e}")
        raise
