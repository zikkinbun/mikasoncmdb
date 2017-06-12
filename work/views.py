# _*_ coding:utf-8_*_
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, ManualScript, UploadScript, ServerUser
from .serializers import ServerUserSerializers

import json
import os
import datetime

class ServerUserApi(APIView):
    """
        list all servers or create a server
    """

    def get(self, request, format=None):
        users = ServerUser.objects.all()
        serializer = ServerUserSerializers(users, many=True)
        return Response(serializer.data)

@csrf_exempt
def edit_file(request):
    if request.method == 'POST':
        origin = request.POST.get('origin', '')
        path = ''
        if origin == 1 or origin == '1':
            name = request.POST.get('name', '')
            user = request.POST.get('user', '')
            content = request.POST.get('content', '')
            params = request.POST.get('params', '')
            destination = default_storage.save('./file/' + name + '.sh', ContentFile(content))
            if default_storage.exists(destination):
                path = os.path.join('./file', name + '.sh')
                file = ManualScript.objects.create(name=name, params=params, content=content, path=path)
            else:
                msg = {
                    'retcode': '-2',
                    'retmsg': '文件保存失败'
                }
                return HttpResponse(msg)
            msg = {
                'retcode': '1',
                'retmsg': '文件记录创建成功'
                }
            return HttpResponse(msg)


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('myfile', None)
        if not file:
            return HttpResponseBadRequest("request not valid")
        filename = file.name
