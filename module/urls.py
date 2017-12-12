from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers

from .views import CreateModule, GetModule, CreateModuleDetail, GetModuleDetail, SetModuleDetail, \
    SetModuleServer, DeleteModule, ActiveDetail, SetModule

urlpatterns = [
    url(r'^CreateModule$', CreateModule.as_view()),
    url(r'^GetModule$', GetModule.as_view()),
    url(r'^SetModule$', SetModule.as_view()),
    url(r'^DelModule$', DeleteModule.as_view()),
    url(r'^CreateModuleDetail$', CreateModuleDetail.as_view()),
    url(r'^GetModuleDetail$', GetModuleDetail.as_view()),
    url(r'^SetModuleDetail$', SetModuleDetail.as_view()),
    url(r'^ActiveDetail$', ActiveDetail.as_view()),
    url(r'^SetModuleServer$', SetModuleServer.as_view()),
]
