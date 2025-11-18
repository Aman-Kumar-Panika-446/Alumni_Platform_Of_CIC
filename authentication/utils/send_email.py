import requests, os
def send_otp_to_mail(email, otp_code):
    api_key = os.getenv("EMAIL_API_KEY")
    url = os.getenv("EMAIL_API_URL")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "from": {"email": "CIC@test-eqvygm01nzjl0p7w.mlsender.net"},
        "to": [{"email": email}],
        "subject": "Your OTP Code",
        "text": f"Your OTP is: {otp_code}",
        "html": f"<p>Your verification code for Alumni Network Platform is: <strong>{otp_code}</strong></p>"
    }
    
    try: 
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return True 
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {e}")
        return False    
