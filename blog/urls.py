from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<year>[0-9]{4})/(?P<slug>[\w\-]+)/$', views.display, name='display'),
]
