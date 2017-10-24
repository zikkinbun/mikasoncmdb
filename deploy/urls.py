from django.conf.urls import url
from . import period_deploy, gitlab_api, salt_api, record_api, deploy_api

app_name = 'deploy'

urlpatterns = [
    url(r'^GetProjects$', gitlab_api.GetProjects.as_view()),
    url(r'^GetBranchs$', gitlab_api.GetBranchs.as_view()),
    url(r'^GetTags$', gitlab_api.GetTags.as_view()),
    url(r'^GetProjectInfo$', gitlab_api.GetProjectsInfo.as_view()),
    url(r'^SetProjectInfo$', gitlab_api.UpdateProjectInfo.as_view()),
    url(r'^GetRecords$', record_api.GetRecords.as_view()),
    url(r'^PtDeploy$', deploy_api.Deploy.as_view()),
    url(r'^Rollback$', deploy_api.Rollback.as_view()),
    url(r'^PeriodDeploy$', period_deploy.PeriodDeploy.as_view()),
]
