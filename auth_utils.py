import re
import random
import smtplib
from email.message import EmailMessage
from passlib.hash import bcrypt

def validate_password(password):
    """
    Validate password strength against security requirements
    
    Requirements:
    - Minimum 7 characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character (!@#$%^&*)
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (bool: is_valid, str: message)
    """
    if not password or len(password) < 7:
        return False, "❌ Password too short (minimum 7 characters required)"
    
    if not re.search(r"[A-Z]", password):
        return False, "❌ Password must contain at least 1 uppercase letter"
    
    if not re.search(r"[0-9]", password):
        return False, "❌ Password must contain at least 1 number"
    
    if not re.search(r"[!@#$%^&*()_+=\-\[\]{};:'\",.<>?/\\|`~]", password):
        return False, "❌ Password must contain at least 1 special character"
    
    return True, "✅ Password meets security requirements"


def hash_password(password):
    """
    Hash password using bcrypt for secure storage
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return bcrypt.hash(password)


def verify_password(password, hashed):
    """
    Verify password against hashed version
    
    Args:
        password: Plain text password to verify
        hashed: Hashed password from database
        
    Returns:
        bool: True if password matches
    """
    return bcrypt.verify(password, hashed)


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email address string
        
    Returns:
        tuple: (bool: is_valid, str: message)
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, "❌ Email is required"
    
    if not re.match(email_pattern, email):
        return False, "❌ Invalid email format"
    
    return True, "✅ Valid email"


def generate_otp():
    """
    Generate a 6-digit OTP
    
    Returns:
        str: 6-digit OTP
    """
    return str(random.randint(100000, 999999))


def send_otp(receiver_email, sender_email=None, sender_password=None, otp=None):
    """
    Send OTP via email for verification
    
    Args:
        receiver_email: Recipient email address
        sender_email: Sender Gmail address (optional)
        sender_password: Gmail app password (optional)
        otp: OTP code (if None, generates new one)
        
    Returns:
        str or None: OTP if sent successfully, None if failed
    """
    if otp is None:
        otp = generate_otp()
    
    # If sender credentials not provided, return OTP for testing
    # In production, you'd require these
    if not sender_email or not sender_password:
        print(f"[DEV MODE] OTP for {receiver_email}: {otp}")
        return otp
    
    try:
        msg = EmailMessage()
        msg.set_content(f"""
        Welcome to PennyWyse AI!
        
        Your verification code is: {otp}
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        PennyWyse AI Team
        """)
        
        msg['Subject'] = 'PennyWyse AI - Verification Code'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        
        return otp
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Gmail authentication failed. Check email/password or enable 'App Passwords'")
        return None
    except smtplib.SMTPException as e:
        print(f"Error sending email: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


def validate_phone(phone):
    """
    Validate Indian phone number format
    
    Args:
        phone: Phone number string
        
    Returns:
        tuple: (bool: is_valid, str: message)
    """
    # Remove spaces and common separators
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for valid Indian phone number (10 digits, optionally with +91 or 0)
    pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
    
    if not re.match(pattern, phone_clean):
        return False, "❌ Invalid phone number (must be 10 digits starting with 6-9)"
    
    return True, "✅ Valid phone number"


def sanitize_input(text, max_length=500):
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>\"\'%;()&+]', '', str(text))
    
    # Limit length
    text = text[:max_length]
    
    # Strip whitespace
    text = text.strip()
    
    return text