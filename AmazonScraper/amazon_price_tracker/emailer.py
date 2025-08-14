import smtplib
import ssl
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL



def send_email(product_name, product_url, current_price):
    subject = f"Price Drop Alert: {product_name}"
    body = (
        f"The price for '{product_name}' has dropped to ${current_price:.2f}!\n\n"
        f"Check it out here: {product_url}"
    )

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")