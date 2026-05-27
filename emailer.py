import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body, file_path):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['From'] = email_address
    msg['To'] = os.getenv("TO_EMAIL")
    msg['Subject'] = subject
    msg.set_content(body)

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)