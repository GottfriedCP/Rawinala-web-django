from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from .models import Article, Tag

# Create your views here.
def home(request):
    request.session['curr_page'] = 'blog'
    art_list = Article.objects.filter(publish_status=True).order_by('-time_created')
    paginator = Paginator(art_list, 20, orphans=3)
    page = request.GET.get('page')

    try:
        arts = paginator.page(page)
    except PageNotAnInteger:
        arts = paginator.page(1)
    except EmptyPage:
        arts = paginator.page(paginator.num_pages)

    context = {
        'art_list': art_list, # Used for checking only, may be revised later
        'arts': arts,
    }
    return render(request, 'blog/index.html', context)

def display(request, year, slug):
    request.session['curr_page'] = 'blog'
    art = get_object_or_404(Article, time_created__year=year, slug=slug)
    art_tags = Tag.objects.filter(article=art.id)

    context = {
        'art': art,
        'tags': art_tags,
        'debug': settings.DEBUG,
    }
    response =  render(request, 'blog/view_article.html', context)

    if request.COOKIES.get("view_%s" % str(art.uuid)) is None and not request.user.is_authenticated:
        import datetime
        response.set_cookie("view_%s" % str(art.uuid), value=str(art.title), expires=(datetime.datetime.now()+datetime.timedelta(days=2)))
        art.views += 1
        art.save()

    return response
