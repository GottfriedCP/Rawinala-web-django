from django.shortcuts import render, redirect
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import rawinala_project.secrets as secret
import datetime
from .forms import NewsletterForm
from .models import Subscriber, Newsletter

# Create your views here.
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Create new subscriber
            subscriber = Subscriber(email=email)
            subscriber.save()

            # Send greetings
            subject = 'Rawinala - Newsletter Subscription'
            message = 'Hello,\n\nThis email is sent to you because you have just subscribed to our newsletter.\n\nTo unsubscribe, please click this link: www.rawinala.org/newsletter/unsubscribex/%s' % (subscriber.uuid)
            sender = 'Rawinala.org <%s>' % (secret.EMAIL_HOST_USER)
            send_mail(subject, message, sender, [email])
            messages.success(request, 'Subscription successful.')
        except Exception as ex:
            print(ex)
            messages.error(request, 'Subscription failed.')

        return redirect('rawinala:home')

def unsubscribe(request, uuid):
    try:
        # Delete subscriber
        subscriber = Subscriber.objects.get(uuid=uuid)
        subscriber.delete()
        messages.success(request, 'You have been Unsubscribed.')
    except Exception as ex:
        print(ex)
        messages.error(request, 'Unsubscription failed. Please contact administrator for help.')
    return redirect('rawinala:home')

@login_required
def create(request):
    if request.session.get('curr_page', False):
        del request.session['curr_page']
    
    # Show newsletter creation form
    newsletter_edition = datetime.datetime.now()
    content_form = NewsletterForm()

    context = {
        'edition': newsletter_edition,
        'content_form': content_form,
    }
    return render(request, 'newsletter/create_newsletter.html', context)

@login_required
def publish(request):
    if request.method == 'POST':
        content_form = NewsletterForm(request.POST)
        if content_form.is_valid():
            content = content_form.cleaned_data['content']

            try:
                # Save to database
                newsletter = Newsletter(content=content, author=request.user)
                # Get subscriber list
                recipients = Subscriber.objects.all()
                datatuple = []
                for recipient in recipients:
                    subject = 'Sapa Sahabat Rawinala'
                    context = {
                        'edition': datetime.datetime.now(),
                        'content': content,
                        'recipient': recipient,
                    }
                    message_html = render_to_string('newsletter/newsletter.html', context)
                    sender = 'Rawinala.org <%s>' % (secret.EMAIL_HOST_USER)
                    to = [recipient.email]
                    row = (subject, strip_tags(message_html), message_html, sender, to)
                    datatuple.append(row)
                datatuple = tuple(datatuple)
                send_mass_html_mail(datatuple)
            except Exception as ex:
                print(ex)

        else:
            context = {
                'content_form': content_form,
            }
            return render(request, 'newsletter/create_newsletter.html', context)

    return redirect('rawinala:home')

def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.
    By semente (https://stackoverflow.com/a/10215091/6012465)
    """
    connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
    
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)
