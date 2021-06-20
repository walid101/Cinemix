from django import urls
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.home, name="home"),
    path('page', views.page, name="page"),
]
