from django.utils.html import strip_tags
import requests
import rawinala_project.secrets as secret

def send_mail(to, subject, message):
    """Send single mail with txt content."""
    requests.post(
        "https://api.mailgun.net/v3/mg.rawinala.org/messages",
        auth = ('api', secret.MAILGUN_APIKEY),
        data = {
            'from': 'Rawinala.org <no-reply@mg.rawinala.org>',
            'to': [to],
            'subject': subject,
            'text': message
        }
    )

def subscribe(email, uuid):
    """Add email to mailing list."""
    status = requests.post(
        "https://api.mailgun.net/v3/lists/ns_sc@mg.rawinala.org/members",
        auth = ('api', secret.MAILGUN_APIKEY),
        data = {
            'subscribed': True,
            'address': email,
            'vars': '{"uuid": "%s"}' % uuid
        }
    )
    print(status)

def unsubscribe(email):
    """Unsubscribe from newsletter mailing list."""
    requests.delete(
        "https://api.mailgun.net/v3/lists/ns_sc@mg.rawinala.org/members/%s" % email,
        auth = ('api', secret.MAILGUN_APIKEY)
    )

def send_newsletter(html):
    """Publish newsletter, send it to readers."""
    requests.post(
        "https://api.mailgun.net/v3/mg.rawinala.org/messages",
        auth = ('api', secret.MAILGUN_APIKEY),
        data = {
            'from': 'Rawinala.org <newsletter@mg.rawinala.org>',
            'to': ['ns_sc@mg.rawinala.org'],
            'subject': 'Sapa Sahabat Rawinala',
            'text': strip_tags(html),
            'html': html
        }
    )
