from decouple import config, Csv
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from language_setter.language_setter import set_template_language
from blog.models import Article
import random, requests

def home(request):
    request.session['current_page'] = 'home'
    arts = Article.objects.filter(published=True)[:7]

    # get template based on language
    template_name = set_template_language('home/index', request.session.get('language'))
    return render(request, template_name, {
        'recent_arts': arts,
    })

def about(request):
    if request.method == 'POST':
        captcha_response = request.POST.get('captcha-response')
        if int(captcha_response) != request.session.get('challenge-answer'):
            messages.error(request, 'ERROR: Incorrect challenge response.')
        else:
            visitor_name = request.POST.get('name')
            visitor_email = request.POST.get('email')
            message = request.POST.get('message')

            email = EmailMessage(
                f'Pesan dari {visitor_name}',
                message,
                f'{visitor_name} via Rawinala.org <{settings.EMAIL_HOST_USER}>',
                settings.ADMINS_EMAIL,
                reply_to=[visitor_email],
            )
            try:
                email.send()
                messages.success(request, 'Message sent.')
            except:
                messages.error(request, 'ERROR: Message not sent.')
        return redirect('home:about')
    
    # Just show the About page
    request.session['current_page'] = 'about'

    opr1 = random.randint(30, 50)
    opr2 = random.randint(1, 29)
    opn = '+' if random.randint(1, 2) == 1 else '-'
    challenge = f'{opr1} {opn} {opr2}'
    request.session['challenge-answer'] = (opr1 + opr2) if opn == '+' else (opr1 - opr2)
    template_name = set_template_language('home/about', request.session.get('language'))
    return render(request, template_name, {
        'challenge': challenge,
    })

def donation(request, code=None):
    request.session['current_page'] = 'donation'
    if code == settings.THANKS_CODE:
        return render(request, 'home/donation_success.html')
    template_name = set_template_language('home/donation', request.session.get('language'))
    return render(request, template_name)

def login_view(request):
    if request.method == 'POST':
        # Check ReCaptcha validity
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': config('RECAPTCHA'),
            'response': request.POST.get('g-recaptcha-response', False),
        })
        if not r.json().get('success', False):
            print('Error: Recaptcha response invalid')
            return redirect('home:login')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.session.get('redirect_to', False)
            if redirect_to:
                return redirect(redirect_to)
            return redirect('/')
    
    request.session['current_page'] = None
    request.session['redirect_to'] = request.GET.get('next', False)
    return render(request, 'home/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home:home')

@login_required
def admin_menu(request):
    return render(request, 'home/admin-menu.html')

def set_language(request):
    if request.method == 'POST':
        request.session['language'] = request.POST.get('language')
        redirect_to = request.POST.get('redirect_to')

        return redirect(redirect_to)
