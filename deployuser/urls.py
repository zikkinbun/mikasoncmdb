from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'deployuser'
urlpatterns = [
    url(r'^login/', views.login, name='login'),
]
