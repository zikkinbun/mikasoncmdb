from django.conf.urls import url
from . import views, gitlab_api, salt_api

app_name = 'deploy'

urlpatterns = [
    url(r'^GetProjects$', gitlab_api.GetProjects.as_view()),
    url(r'^GetBranchs$', gitlab_api.GetBranchs.as_view()),
    url(r'^GetTags$', gitlab_api.GetTags.as_view()),
    url(r'^pushTest$', views.PushTest.as_view()),
    url(r'^pushProd$', views.PushProd.as_view()),
]
