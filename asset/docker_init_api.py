#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from celery import task

from .serializers import DockerContainerSerializers
from .models import Docker_Container, Docker_Image

import requests
import json
import time

@task
def check_containers():
    dockerd_url = 'http://112.74.182.80:4243/containers/json?all=1'
    # if request.method == 'GET':
    headers = {'Content-Type': 'application/json'}
    r = requests.get(dockerd_url, headers=headers)
    datas = r.json()
    containers = []
    status = None
    current_containers = Docker_Container.objects.all()
    if len(datas) != len(current_containers):
            # current_containers.delete()
        for data in datas:
            x = time.localtime(data['Created'])
            created = time.strftime('%Y-%m-%d %H:%M:%S', x)
            if data['State'] == 'running':
                status = 0
            else:
                status = 1
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
        return contain
    else:
        for data in datas:
            x = time.localtime(data['Created'])
            created = time.strftime('%Y-%m-%d %H:%M:%S', x)
            if data['State'] == 'running':
                status = 0
            else:
                status = 1
            container = {
                'id': data['Id'][:12],
                'Name': data['Names'][0],
                'Image': data['Image'],
                'Command': data['Command'],
                'Created': created,
                'Status': data['State']
                }
            containers.append(container)
            remain_container = Docker_Container.objects.filter(containerId=container['id'])
            remain_container.update(status=data['State'])
        contain = json.dumps(containers)
        return contain

@task
def check_images():
    dockerd_url = 'http://112.74.182.80:4243/images/json?all=0'
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
    return local_image

@csrf_exempt
def container_stat(request):
    if request.method == 'POST':
        # containerId = json.loads(request.body)['containerId']
        containerId = request.POST.get('containerId', '')
        dockerd_url = 'http://112.74.182.80:4243/containers/%s/stats' % containerId
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

@csrf_exempt
def stop_container(request):
    if request.method == 'POST':
        # containerId = json.loads(request.body)['containerId']
        containerId = request.POST.get('containerId', '')
        print containerId
        dockerd_url = 'http://112.74.182.80:4243/containers/%s/stop' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.post(dockerd_url, headers=headers)
        code = r.status_code
        if code == 200 or code == '200':
            msg = {
                'retmsg': 'container have stoped'
            }
            return HttpResponse(json.dumps(msg))
        else:
            return Http404

@csrf_exempt
def start_container(request):
    if request.method == 'POST':
        # containerId = json.loads(request.body)['containerId']
        containerId = request.POST.get('containerId', '')
        print containerId
        dockerd_url = 'http://112.74.182.80:4243/containers/%s/start' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.post(dockerd_url, headers=headers)
        code = r.status_code
        if code == 200 or code == '200':
            msg = {
                'retmsg': 'container have started'
            }
            return HttpResponse(json.dumps(msg))
        else:
            return Http404

@csrf_exempt
def delete_container(request):
    if request.method == 'POST':
        # containerId = json.loads(request.body)['containerId']
        containerId = request.POST.get('containerId', '')
        dockerd_url = 'http://112.74.182.80:4243/containers/%s' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.delete(dockerd_url)
        code = r.status_code
        if code == 200 or code == '200':
            msg = {
                'retmsg': 'container have deleted'
            }
            return HttpResponse(json.dumps(msg))
        else:
            return Http404
