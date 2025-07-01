import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_email(to_email: str, reset_link: str):
    smtp_server = "smtp.example.com"  # Update with your SMTP server
    smtp_port = 587
    smtp_user = "your@email.com"      # Update with your email
    smtp_password = "yourpassword"    # Update with your password

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
