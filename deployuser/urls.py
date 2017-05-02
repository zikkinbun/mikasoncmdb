from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views
from views import login

app_name = 'deployuser'
urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
