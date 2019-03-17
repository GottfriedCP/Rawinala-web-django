from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_all, name='list'),
    path('<int:year>/<slug>/', views.view_article, name='article'),

    path('create/', views.create, name='create'),
    path('<int:year>/<slug>/edit/', views.edit, name='edit'),
]
