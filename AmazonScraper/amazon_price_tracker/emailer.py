import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "allenjosh1983@gmail.com"
EMAIL_PASSWORD = "drhh uuua mbwl rbji"  # ✅ Use Gmail App Password

def send_email(product_name, url, price):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = f"Price Alert: {product_name} is now ${price}"

        body = f"The price for {product_name} has dropped to ${price}.\nCheck it out: {url}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("📧 Email sent successfully")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")