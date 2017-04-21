from django.conf.urls import url
from . import views, gitlab_api, salt_api

app_name = 'api'

urlpatterns = [
    url(r'^getproject/$', gitlab_api.get_project, name='get_project'),
    url(r'^getbranches/$', gitlab_api.get_branches, name='get_branches'),
    url(r'^gettags/$', gitlab_api.get_tag, name='get_tag'),
    url(r'^pushTest/$', views.pushTest, name='pushTest'),
    url(r'^pushProd/$', views.pushTest, name='pushProd'),
]
