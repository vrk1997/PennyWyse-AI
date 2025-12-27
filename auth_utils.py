import re
import random
import smtplib
from email.message import EmailMessage

def validate_password(password):
    # Rule: 7+ chars, 1 Cap, 1 Num, 1 Special
    if len(password) < 7:
        return False, "Password too short (min 7 chars)."
    if not re.search(r"[A-Z]", password):
        return False, "Need at least 1 capital letter."
    if not re.search(r"[0-9]", password):
        return False, "Need at least 1 number."
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Need at least 1 special character."
    return True, "Success"

def send_otp(receiver_email, sender_email, sender_password):
    otp = str(random.randint(100000, 999999))
    msg = EmailMessage()
    msg.set_content(f"Your WealthFlow verification code is: {otp}")
    msg['Subject'] = 'Verification Code'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # This connects to your future Gmail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return otp
    except Exception as e:
        return None