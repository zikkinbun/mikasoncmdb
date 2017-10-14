from django.conf.urls import url
from . import onekey_deploy_api, gitlab_api, salt_api, record_api, deploy_api

app_name = 'deploy'

urlpatterns = [
    url(r'^GetProjects$', gitlab_api.GetProjects.as_view()),
    url(r'^GetBranchs$', gitlab_api.GetBranchs.as_view()),
    url(r'^GetTags$', gitlab_api.GetTags.as_view()),
    url(r'^GetProjectInfo$', gitlab_api.GetProjectsInfo.as_view()),
    url(r'^SetProjectInfo$', gitlab_api.UpdateProjectInfo.as_view()),
    url(r'^GetRecords$', record_api.GetRecords.as_view()),
    url(r'^pushTest$', onekey_deploy_api.PushTest.as_view()),
    url(r'^pushProd$', onekey_deploy_api.PushProd.as_view()),
    url(r'^PtDeploy$', deploy_api.Deploy.as_view()),
]
