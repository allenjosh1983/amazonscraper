import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL


def send_email(recipient, product_name, url, current_price):
    sender = EMAIL_ADDRESS
    password = EMAIL_PASSWORD
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = f"Price Alert: {product_name}"
    body = f"The price for {product_name} has dropped to ${current_price:.2f}!\n{url}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")