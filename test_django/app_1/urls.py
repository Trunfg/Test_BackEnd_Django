# todo/todo_api/urls.py : API urls.py
# from django.conf.urls import url
from django.urls import path
from .views import (
    MainView, AboutView
)

urlpatterns = [
    path('', MainView.as_view(), name='main'),

    path('about/', AboutView.as_view(), name='about'),
]