from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, renderers
from . import server_api_views, docker_init_api, cluster_api_views

urlpatterns = [
    url(
        r'^ListServer$',
        server_api_views.ListAllServer.as_view()
    ),
    url(
        r'^ListServerName$',
        server_api_views.ListServerName.as_view()
    ),
    url(
        r'^CreateServer$',
        server_api_views.CreateServer.as_view()
    ),
    url(
        r'^EditServer$',
        server_api_views.EditServer.as_view()
    ),
    url(
        r'^EditServerMonitor$',
        server_api_views.EditServerMonitor.as_view()
    ),
    url(
        r'^DeleteServer$',
        server_api_views.DeleteServer.as_view()
    ),
    url(
        r'^CreateDetail$',
        server_api_views.CreateServerDetail.as_view()
    ),
    url(
        r'^ListDetail$',
        server_api_views.ListServerAllDetail.as_view()
    ),
    url(
        r'^GetDetail$',
        server_api_views.GetServerDetail.as_view()
    ),
    url(
        r'^EditDetail$',
        server_api_views.EditServerDetail.as_view()
    ),
    url(
        r'^EditServerDetail$',
        server_api_views.EditServerAndDetail.as_view()
    ),
    url(
        r'^CreateService$',
        server_api_views.CreateServerSevice.as_view()
    ),
    url(
        r'^GetService$',
        server_api_views.GetServerService.as_view()
    ),
    url(
        r'^EditService$',
        server_api_views.EditServerSevice.as_view()
    ),
    url(
        r'^DeleteService$',
        server_api_views.DeleteServerService.as_view()
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
        r'^DeleteImages$',
        docker_init_api.DeletaSwarmImages.as_view()
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
    url(
        r'^SetServerFunc$',
        server_api_views.ServerFuncRelation.as_view(),
    ),
    url(
        r'^EditServerFunc$',
        server_api_views.UpdateActive.as_view(),
    ),
    url(
        r'^GetServerFunc$',
        server_api_views.GetServerFunc.as_view(),
    ),
    url(
        r'^CreateCluster$',
        cluster_api_views.CreateCluster.as_view(),
    ),
    url(
        r'^GetCluster$',
        cluster_api_views.GetCluster.as_view(),
    ),
    url(
        r'^SetCluster$',
        cluster_api_views.SetCluster.as_view(),
    ),
    url(
        r'^DelCluster$',
        cluster_api_views.DelCluster.as_view(),
    ),
    url(
        r'^BindServer$',
        cluster_api_views.BindClusterServer.as_view(),
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
