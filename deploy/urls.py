from django.conf.urls import url
from . import views, gitlab_api, salt_api

app_name = 'api'

urlpatterns = [
    url(r'^getproject/$', gitlab_api.get_project, name='get_project'),
    url(r'^getbranches/$', gitlab_api.get_branches, name='get_branches'),
    url(r'^gettags/$', gitlab_api.get_tag, name='get_tag'),
    # url(r'^dict_init/$', views.dict_init, name='dict_init'),
    # url(r'^dict_move/$', views.dict_move, name='dict_move'),
    # url(r'^dict_tar/$', views.dict_tar, name='dict_tar'),
    # url(r'^dict_upload/$', views.dict_upload, name='dict_upload'),
    # url(r'^dict_config/$', views.dict_config, name='dict_config'),
    # url(r'^file_config/$', views.file_config, name='file_config'),
    # url(r'^service_init/$', views.service_init, name='service_init'),
    url(r'^pushTest/$', views.pushTest, name='pushTest'),
    url(r'^pushProd/$', views.pushProd, name='pushProd'),
]
