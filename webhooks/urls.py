from django.conf.urls import url, include
from . import views

# app_name = 'git_web'
urlpatterns = [
    url(r'^$', views.index, name='index' ),
]
