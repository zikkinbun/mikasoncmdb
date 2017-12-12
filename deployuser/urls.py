from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from rest_framework_jwt.views import verify_jwt_token, refresh_jwt_token, obtain_jwt_token
from rest_framework.authtoken.views import obtain_auth_token

from .views import LoginAccount, CreateAccount, GetAccountAll

app_name = 'deployuser'

urlpatterns = [
    url(r'^addUser$', CreateAccount.as_view()),
    url(r'^getUser$', GetAccountAll.as_view()),
    url(r'^login$', LoginAccount.as_view()),
    url(r'^getJwtToken$', obtain_jwt_token),
    url(r'^getToken$', obtain_auth_token),
    # url(r'^resToken$', refresh_jwt_token),
]
