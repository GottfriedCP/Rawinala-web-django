from django.shortcuts import render, redirect #get_object_or_404, get_list_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import rawinala_project.secrets as secret
from .models import Message
from blog.models import Article

# Create your views here.

def home(request):
    request.session['curr_page'] = 'home'
    context = {}

    # Check recent articles
    recent_articles = Article.objects.filter(publish_status=True).order_by('-time_created')[0:5]
    context['recent_arts'] = recent_articles

    # Check if newsletter subscription is successful
    subscribe_status = request.session.get('subscribe_status')
    if subscribe_status is not None:
        context['subscribe_status'] = (subscribe_status == 1)
        del request.session['subscribe_status']
    
    return render(request, 'rawinala/index.html', context)

def donation(request, code=None):
    request.session['curr_page'] = 'donation'
    if code == secret.THANKS_CODE:
        return render(request, 'rawinala/donation_success.html')
    return render(request, 'rawinala/donation.html')

def about(request):
    request.session['curr_page'] = 'about'
    from random import randint
    captcha1 = randint(16, 30)
    captcha2 = randint(1, 15)
    operation = randint(1, 2)
    if operation == 1: # Addition
        challenge = '%s + %s =' % (captcha1, captcha2)
        request.session['captcha_answer'] = captcha1 + captcha2
    else:
        challenge = '%s - %s =' % (captcha1, captcha2)
        request.session['captcha_answer'] = captcha1 - captcha2
    
    context = {
        'challenge': challenge,
    }
    return render(request, 'rawinala/about.html', context)

def contact(request):
    if request.method == 'POST':
        # Validate captcha
        if request.session['captcha_answer'] == int(request.POST.get('captcha-response')):
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            try:
                # Save message to database
                m = Message(name=name, email=email, content=message.strip())
                m.save()
                # Send email to admins (using SMTP)
                subject = 'Message from %s' % (name)
                sender = '%s (via Rawinala.org)' % (name)
                message = 'Name: %s\nPlease reply to this address: %s\n\n%s' % (name, email, message)
                sender_email = 'Rawinala.org <%s>' % (secret.EMAIL_HOST_USER)
                recipients = secret.recipients
                send_mail(subject, message, sender_email, recipients)
                messages.success(request, 'Message sent successfully.')
            except Exception as ex:
                print(ex)
                messages.error(request, 'Failed to send message.')
        else:
            messages.error(request, 'Captcha error.')
        
    return redirect('rawinala:about')

@login_required
def message(request):
    if request.session.get('curr_page', False):
        del request.session['curr_page']
    
    # Query all visitor messages
    visitor_message_list = Message.objects.order_by('-time')
    # using paginator to list 50 per page
    paginator = Paginator(visitor_message_list, 50, orphans=5)
    page = request.GET.get('page')
    try:
        visitor_messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not int, deliver first page
        visitor_messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        visitor_messages = paginator.page(paginator.num_pages)

    context = {
        'visitor_messages': visitor_messages,
    }
    return render(request, 'rawinala/message_list.html', context)

def login_view(request):
    if request.session.get('curr_page', False):
        del request.session['curr_page']
    
    if request.user.is_authenticated:
        return redirect('rawinala:home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.session.get('next_redir', False):
                next_redir = request.session['next_redir']
                del request.session['next_redir']
                return redirect(next_redir)
            else:
                return redirect('rawinala:home')
    
    
    # GET request
    if request.GET.get('next', False):
        request.session['next_redir'] = request.GET.get('next')
    return render(request, 'rawinala/login.html')

def logout_view(request):
    if request.session.get('msg_count', False):
        del request.session['msg_count']
    logout(request)
    return redirect('rawinala:home')
