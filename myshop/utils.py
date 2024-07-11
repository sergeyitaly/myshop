import requests
from django.conf import settings

def send_mailgun_email(to_email, subject, body):
    try:
        domain = settings.MAILGUN_DOMAIN
        api_key = settings.MAILGUN_API_KEY
        from_email = settings.DEFAULT_FROM_EMAIL

        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": from_email,
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
