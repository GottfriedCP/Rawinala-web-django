from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, send_mail, EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import NewsletterForm
from .models import Subsr

def create(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            title = None if form.cleaned_data['title'] == '' else form.cleaned_data['title']
            date_created = form.cleaned_data['date_created']
            content = form.cleaned_data['content']
            content = content.replace('src="/', f'src="http://{request.get_host()}/')
            content = content.replace('href="/', f'href="http://{request.get_host()}/')

            subsrs = Subsr.objects.all()
            email_object_list = []
            for subsr in subsrs:
                email = EmailMessage(
                    subject='Sapa Sahabat Rawinala',
                    body=render_to_string('newsletter/newsletter.html', {
                        'title': title,
                        'date_created': date_created,
                        'content': content,
                        'hostname': request.get_host(),
                        'unsubs_path': subsr.get_unsubscribe_path(),
                    }),
                    from_email=f'Rawinala.org <{settings.EMAIL_HOST_USER}>',
                    to=[subsr.email],
                )
                email.content_subtype = 'html'
                email_object_list.append(email)
            connection = get_connection()
            connection.send_messages(email_object_list)
            print('Newsletters sent.')
        return redirect('home:home')

    form = NewsletterForm()
    return render(request, 'newsletter/create-newsletter.html', {
        'form': form,
    })

def publish(request):
    pass

def subs(request):
    """Handles new subscription."""
    if request.method == 'POST':
        subsr_email = request.POST.get('email')

        if Subsr.objects.filter(email=subsr_email).count() > 0:
            messages.error(request, 'ERROR: Email already exists.')
        else:
            subsr = Subsr(email=subsr_email)
            subsr.save()
            # Send greetings message
            unsubsribe_code = 'test' if settings.DEBUG else subsr.id
            if _send_greetings(request.get_host(), subsr.email, unsubsribe_code):
                messages.success(request, 'You have been subscribed successfully.')
        return redirect('home:home')

def unsubs(request, id):
    """Handles un-subscription."""
    subsr = get_object_or_404(Subsr, id=id)
    print(f'Deleted {subsr.delete()[0]} subscriber.')
    messages.success(request, 'You have been un-subscribed successfully.')
    return redirect('home:home')

def _send_greetings(hostname, email, code='test'):
    try:
        send_mail(
            'Newsletter Subscription',
            f'''Thank you for subscribing to 'Sapa Sahabat Rawinala'.
            To un-subscribe, click here:
            http://{hostname}{reverse('newsletter:unsubscribe', args=[code])}
            ''',
            f'Sapa Sahabat Rawinala <{settings.EMAIL_HOST_USER}>',
            [email],
            fail_silently=False,
        )
    except:
        print('ERROR: cannot send greeting email.')
        return False
    return True
