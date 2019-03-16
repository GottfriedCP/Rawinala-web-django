from django.urls import path
from newsletter import views

app_name = 'newsletter'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('publish/', views.publish, name='publish'),
    path('subscribe/', views.subs, name='subscribe'),
    path('unsubscribe/<code>', views.unsubs, name='unsubscribe'),
]
