from django.conf.urls import url
from . import onekey_deploy_api, gitlab_api, salt_api

app_name = 'deploy'

urlpatterns = [
    url(r'^GetProjects$', gitlab_api.GetProjects.as_view()),
    url(r'^GetBranchs$', gitlab_api.GetBranchs.as_view()),
    url(r'^GetTags$', gitlab_api.GetTags.as_view()),
    url(r'^GetProjectInfo$', gitlab_api.GetProjectsInfo.as_view()),
    url(r'^SetProjectInfo$', gitlab_api.UpdateProjectInfo.as_view()),
    url(r'^pushTest$', onekey_deploy_api.PushTest.as_view()),
    url(r'^pushProd$', onekey_deploy_api.PushProd.as_view()),
]
