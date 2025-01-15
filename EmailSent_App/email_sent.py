from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def email_sent(user, subject, html_message):
    print("(-)"*30)
    from_email = 'NextHire <noreply@nexthire.com>'
    recipient = f"{user.first_name} {user.last_name} <{user.email}>"
    email = EmailMultiAlternatives(subject=subject, from_email=from_email, to=[recipient], 
        body="Please view this email in a client that supports HTML.")
    email.attach_alternative(html_message, 'text/html')
    try:
        email.send()
        print("Email sent successfully to:", user.email)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
    print("(-)"*30)
    return False


def sent_account_registration_activation_email(user):
    template = 'email_templates/account_registration_email_tamplates.html'
    subject = f"Account Registration Confirmation, {user.first_name} {user.last_name}! Welcome to NextHire"
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    activation_url = f"http://localhost:5173/accounts/activate/{uid}/{token}/"

    html_message = render_to_string(f'{template}', {'user': user, 'activation_url': activation_url})
    email_sent(user, subject, html_message)

def sent_password_reset_email(user):
    template = 'email_templates/password_reset_email_tamplates.html'
    subject = f"NextHire: Password Reset Request for { user.first_name } { user.last_name }"
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    password_reset_url = f"http://localhost:5173/accounts/password/reset/{uid}/{token}/"

    html_message = render_to_string(f'{template}', {'user': user, 'password_reset_url': password_reset_url})
    email_sent(user, subject, html_message)