from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers

from .views import CreateBussiness, GetBussiness, DelBussiness, SetBussiness


urlpatterns = [
    url(r'^CreateBussiness$', CreateBussiness.as_view()),
    url(r'^GetBussiness$', GetBussiness.as_view()),
    url(r'^SetBussiness$', SetBussiness.as_view()),
    url(r'^DelBussiness$', DelBussiness.as_view()),
]
