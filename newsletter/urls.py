from django.conf.urls import url, include
from . import views

app_name = 'newsletter'
urlpatterns = [
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^unsubscribex/(?P<uuid>[\w]{96})/$', views.unsubscribe, name='unsubscribe'),
    url(r'^create/$', views.create, name='create'),
    url(r'^publish/$', views.publish, name='publish'),
]