#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import DockerContainerSerializers
from .models import Docker_Container, Docker_Image

import requests
import json
import time

@csrf_exempt
def check_containers(request):
    dockerd_url = 'http://112.74.182.80:4243/containers/json'
    if request.method == 'GET':
        headers = {'Content-Type': 'application/json'}
        r = requests.get(dockerd_url, headers=headers)
        datas = r.json()
        containers = []
        current_containers = Docker_Container.objects.all()
        if len(datas) != len(current_containers):
            # current_containers.delete()
            for data in datas:
                x = time.localtime(data['Created'])
                created = time.strftime('%Y-%m-%d %H:%M:%S', x)
                container = {
                    'id': data['Id'][:12],
                    'Name': data['Names'][0],
                    'Image': data['Image'],
                    'Command': data['Command'],
                    'Created': created,
                    'Status': data['State']
                    }
                containers.append(container)
                current_containers.update_or_create(hostName='gdr_dev', containerId=container['id'], containerName=data['Names'][0], imageName=data['Image'], \
                                            command=data['Command'], created=created, status=data['State'])
            contain = json.dumps(containers)
            return HttpResponse(contain)
        else:
            for data in datas:
                x = time.localtime(data['Created'])
                created = time.strftime('%Y-%m-%d %H:%M:%S', x)
                container = {
                    'id': data['Id'][:12],
                    'Name': data['Names'][0],
                    'Image': data['Image'],
                    'Command': data['Command'],
                    'Created': created,
                    'Status': data['State']
                    }
                containers.append(container)
                current_containers.update(status=data['State'])
            contain = json.dumps(containers)
            return HttpResponse(contain)

@csrf_exempt
def check_images(request):
    dockerd_url = 'http://112.74.182.80:4243/images/json?all=0'
    if request.method == 'GET':
        headers = {'Content-Type': 'application/json'}
        r = requests.get(dockerd_url, headers=headers)
        datas = r.json()
        images = []
        current_images = Docker_Image.objects.all()
        for data in datas:
            x = time.localtime(data['Created'])
            created = time.strftime('%Y-%m-%d %H:%M:%S', x)
            y = int(data['Size'])/(1024*1024*8)
            if len(data['RepoTags']) > 1:
                for i in range(len(data['RepoTags'])):
                    image = {
                        'Name': data['RepoTags'][i],
                        'Created': created,
                        'Size': str(y) + ' MB'
                        }
                    images.append(image)
                    current_images.update_or_create(imageName=image['Name'], created=image['Created'], size=image['Size'])
            else:
                image = {
                    'Name': data['RepoTags'][0],
                    'Created': created,
                    'Size': str(y) + ' MB'
                    }
                images.append(image)
                current_images.update_or_create(imageName=image['Name'], created=image['Created'], size=image['Size'])
        local_image = json.dumps(images)
        return HttpResponse(local_image)

@csrf_exempt
def inspect_container(request):
    if request.method == 'POST':
        # containerId = json.loads(request.body)['containerId']
        containerId = request.POST.get('containerId', '')
        dockerd_url = 'http://112.74.182.80:4243/containers/%s/top?ps_args=aux' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.get(dockerd_url, headers=headers)
        datas = r.json()
        payloads = []
        for i in range(len(datas['Processes'])):
            payload = {
                'COMMAND': datas['Processes'][i][-1],
                'CPU': datas['Processes'][i][2],
                'MEM': datas['Processes'][i][3],
            }
            payloads.append(payload)
        return HttpResponse(json.dumps(payloads))
