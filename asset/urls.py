from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from . import asset_api, docker_init_api

urlpatterns = [
    url(
        r'^List$',
        asset_api.ListServer.as_view()
    ),
    url(
        r'^CreateServer$',
        asset_api.CreateServer.as_view()
    ),
    url(
        r'^Detail$',
        asset_api.getServerDetail.as_view()
    ),
    url(
        r'^EditServer$',
        asset_api.EditServerDetail.as_view()
    ),
    url(
        r'^DeleteServer$',
        asset_api.DeleteServer.as_view()
    ),
    url(
        r'^ListSwarmContainers$',
        docker_init_api.ListSwarmContainer.as_view()
    ),
    url(
        r'^ListImages$',
        docker_init_api.ListSwarmImage.as_view()
    ),
    url(
        r'^ContainerDetail$',
        docker_init_api.InspectSwarmContain.as_view(),
    ),
    url(
        r'^StopContainer$',
        docker_init_api.StopSwarmContain.as_view()
    ),
    url(
        r'^StartContainer$',
        docker_init_api.StartSwarmContain.as_view()
    ),
    url(
        r'^DeleteContainer$',
        docker_init_api.DeleteSwarmContain.as_view(),
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
