"""deploySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

# from asset.urls import router

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/', include('deploy.urls', namespace="api")),
    # url(r'^asset/', include(router.urls)),
    url(r'^hooks/', include('webhooks.urls', namespace="webhooks")),
    url(r'^zabbixapi/', include('zabbixapi.urls', namespace="zabbixapi")),
    url(r'^asset/', include('asset.urls', namespace="asset")),
    url(r'^user/', include('deployuser.urls', namespace="user")),
    url(r'^user/admin/', admin.site.urls),
]
