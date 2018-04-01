from django.conf.urls import url, include
from . import views

app_name = 'rawinala'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^donation/$', views.donation, name='donation'),
    url(r'^donation/(?P<code>[\w]+)/$', views.donation, name='donation'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^message/$', views.message, name='message-list'),
    url(r'^message/view/(?P<id>[0-9]+)/$', views.message, name='message-view'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]