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
    url(r'^deploy/', include('deploy.urls', namespace="deploy")),
    url(r'^server/', include('server.urls', namespace="server")),
    url(r'^bussiness/', include('bussiness.urls', namespace="bussiness")),
    url(r'^job/', include('job.urls', namespace="job")),
    url(r'^module/', include('module.urls', namespace="module")),
    url(r'^user/', include('deployuser.urls', namespace="user")),
    url(r'^monitor/', include('monitor.urls', namespace="monitor")),
    url(r'^user/admin/', admin.site.urls),
]
