# _*_ coding:utf-8_*_
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework.views import APIView

from .models import Task, Script
from .serializers import ScriptSerializers, TaskSerializers

import json
import os
import datetime

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('myfile', None)
        destination = ''
        content = ''
        if file:
            if file.mutiple_chunks():
                for chunk in file.chunks():
                    destination = default_storage.save('../files/' + file.name, ContentFile(chunk))
                    # destination.write(chunk)
                # destination.close()
            else:
                destination = default_storage.save('../files/' + file.name, ContentFile(file.read()))
                # destination.close()
            if default_storage.exists(destination):
                name = file.name
                path = os.path.join('../files', file.name)
                origin = json.loads(request.body[u'origin'])
                content = json.loads(default_storage.open(destination).read())
                params = json.loads(request.body[u'origin'])
                Script.objects.create(name=name, path=path, origin=origin, content=content, params=params, created=datetime.datetime.now())
            else:
                msg = {
                    'retcode': -2,
                    'retmsg': '上传的文件不存在，请检查'
                }
                return HttpResponseServerError(msg)
        else:
            msg = {
                'retcode': -1,
                'retmsg': '上传失败'
            }
            return HttpResponseServerError(msg)
