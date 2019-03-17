from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from language_setter.language_setter import set_template_language
from .forms import ArticleForm
from .models import Article

# Create your views here.
def index(request):
    request.session['current_page'] = 'blog'
    art_list = Article.objects.filter(published=True)
    paginator = Paginator(art_list, 7, orphans=3)

    page = request.GET.get('page')
    arts = paginator.get_page(page)
    template_name = set_template_language('blog/index', request.session.get('language'))
    return render(request, template_name, {
        'arts': arts,
    })

@login_required
def list_all(request):
    request.session['current_page'] = 'blog'
    art_list = Article.objects.all()
    paginator = Paginator(art_list, 7, orphans=3)

    page = request.GET.get('page')
    arts = paginator.get_page(page)
    return render(request, 'blog/list-articles.html', {
        'arts': arts,
    })

def view_article(request, year, slug):
    art = get_object_or_404(Article, date_created__year=year, slug=slug)

    template_name = set_template_language('blog/view_article', request.session.get('language'))
    response = render(request, template_name, {
        'art': art,
        'debug': settings.DEBUG,
    })

    if not request.user.is_authenticated and request.COOKIES.get(art.slug) is None:
        import datetime
        now = datetime.datetime.now()
        three_days = now + datetime.timedelta(days=3)
        response.set_signed_cookie(art.slug, art.id, expires=three_days)
        art.view_count = F('view_count') + 1
        art.save()

    return response

@login_required
def create(request):
    request.session['current_page'] = 'blog'
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            art = form.save(commit=False)
            art.content = art.content.replace('src="/', f'src="http://{request.get_host()}/')
            art.save()
            _update_sitemap(request.get_host())
            return redirect(art)

    return render(request, 'blog/create-article.html', {
        'form': form,
    })

@login_required
def edit(request, year, slug):
    art = get_object_or_404(Article, date_created__year=year, slug=slug)
    original_year = art.date_created.year
    original_slug = art.slug
    form = ArticleForm(instance=art)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=art)
        if form.is_valid():
            art = form.save(commit=False)
            art.content = art.content.replace('src="/', f'src="http://{request.get_host()}/')
            art.save()
            _update_sitemap(request.get_host())
            return redirect(art)

    return render(request, 'blog/edit-article.html', {
        'form': form,
        'original_year': original_year,
        'original_slug': original_slug,
    })

def _update_sitemap(hostname):
    """Update sitemap when an article is added/edited/deleted.\n\n
    - hostname: just use 'request.get_host()'
    """
    with open(settings.SITEMAP_LOCATION, 'w') as sitemap:
        homepage = f'https://{hostname}/'
        about_page = f'{homepage}about/'
        blog_page = f'{homepage}blog/'
        donation_page = f'{homepage}donation/'
        sitemap.write(f'{homepage}\n{about_page}\n{blog_page}\n{donation_page}\n')
        
        artsx = Article.objects.filter(published=True)[:9998]
        for artx in artsx:
            sitemap.write(f'https://{hostname}{artx.get_absolute_url()}\n')
