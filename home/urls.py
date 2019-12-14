from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('donation/', views.donation, name='donation'),
    path('donation/<code>', views.donation, name='donation'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-menu/', views.admin_menu, name='admin-menu'),

    path('set-language/', views.set_language, name='set_language'),
]
