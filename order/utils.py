import requests
from django.conf import settings

def send_mailgun_email(to_email, subject, body):
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": [to_email],
                "subject": subject,
                "text": body
            }
        )
        print(f'Mailgun response status: {response.status_code}')
        print(f'Mailgun response body: {response.text}')
        return response
    except Exception as e:
        print(f'Exception in sending email: {e}')
        raise
