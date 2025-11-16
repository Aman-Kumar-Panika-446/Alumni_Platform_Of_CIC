import smtplib, os
import ssl

# Function to send OTP
def send_otp_to_mail(receiver_email, otp):
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")


    subject = "Alumni Connect Platform"
    body = f"Your OTP code is: {otp}"

    message = f"Subject: {subject}\n\n{body}"

    # Gmail SMTP server
    smtp_server = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT_SSL"))

    try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message)
            return True   # success
        
    except Exception as e:
        print("Error sending mail:", e)
        return False  # failure