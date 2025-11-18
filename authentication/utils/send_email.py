import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

def send_otp_to_mail(receiver_email, otp):
    # MailerSend SMTP Configuration
    smtp_host = os.getenv("EMAIL_HOST")
    smtp_port = int(os.getenv("EMAIL_PORT"))
    username = os.getenv("EMAIL_HOST_USER")
    password = os.getenv("EMAIL_HOST_PASSWORD")
    
    # Email details
    from_email = os.getenv("FROM_EMAIL")
    to_email = receiver_email
    subject = 'OTP TO VERIFY ACCOUNT'
    
    # OTP content
    otp_code = otp
    
    # Create message
    message = MIMEMultipart('alternative')
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .otp-code {{ 
                font-size: 32px; 
                font-weight: bold; 
                color: #2563eb; 
                text-align: center; 
                margin: 20px 0;
                padding: 10px;
                background-color: #f3f4f6;
                border-radius: 5px;
                letter-spacing: 5px;
            }}
            .footer {{ 
                margin-top: 30px; 
                font-size: 12px; 
                color: #6b7280; 
                border-top: 1px solid #e5e7eb;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p>Hi</p>
            <p>Greetings!</p>
            <p>Your are just a step away from registering on esteemed Alumni Network Platform of CIC.</p>
            
            <p>Your verification code is:</p>
            
            <div class="otp-code">{otp_code}</div>
            
            <p>Best Regards,</p>
            <p>TEAM CIC</p>
            
            <div class="footer">
                <p>© 2025 Cluster Innovation Centre | Designed By Praman & Asheen Association ❤️.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text content
    text_content = f"""
    OTP For Email Verification
    
    This is a test email from MailerSend SMTP.
    Your OTP for verification is: {otp_code}
    
    This is only a test email.
    
    © 2024 Test Platform. All rights reserved.
    """
    
    # Add both HTML and plain text parts
    message.attach(MIMEText(text_content, 'plain'))
    message.attach(MIMEText(html_content, 'html'))
    
    try:
        # Create SMTP connection
        print("🔌 Connecting to MailerSend SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)

        # Start TLS encryption
        print("🔒 Starting TLS encryption...")
        server.starttls()
        
        # Login to SMTP server
        print("🔑 Logging in to SMTP server...")
        server.login(username, password)
        
        # Send email
        print("📧 Sending test email...")
        server.sendmail(from_email, to_email, message.as_string())
        
        # Close connection
        server.quit()
        print("✅ Email sent successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False