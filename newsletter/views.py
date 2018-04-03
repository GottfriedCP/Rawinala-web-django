from django.shortcuts import render, redirect
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import rawinala_project.secrets as secret
import datetime
import newsletter.mailgun_api as mg
from .forms import NewsletterForm
from .models import Subscriber, Newsletter

# Create your views here.
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Create new subscriber (we need this in database)
            subscriber = Subscriber(email=email)
            subscriber.save()

            # Add to mailing list
            mg.subscribe(email, subscriber.uuid)

            # Send greetings
            subject = 'Rawinala - Newsletter Subscription'
            message = 'Hello,\n\nThis email is sent to you because you have just subscribed to our newsletter "Sapa Sahabat Rawinala".'
            mg.send_mail(email, subject, message)
            messages.success(request, 'Subscription successful.')
        except Exception as ex:
            print(ex)
            messages.error(request, 'Subscription failed.')

        return redirect('rawinala:home')

def unsubscribe(request, uuid):
    try:
        # Delete subscriber from milis and database
        subscriber = Subscriber.objects.get(uuid=uuid)
        subscriber.delete()
        mg.unsubscribe(str(request.GET.get('email')))
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
                newsletter.save()
                # Send newsletter to mailing list
                context = {
                    'edition': datetime.datetime.now(),
                    'content': content,
                }
                message_html = render_to_string('newsletter/newsletter.html', context)
                mg.send_newsletter(message_html)
            except Exception as ex:
                print(ex)

        else:
            context = {
                'content_form': content_form,
            }
            return render(request, 'newsletter/create_newsletter.html', context)

    return redirect('rawinala:home')
