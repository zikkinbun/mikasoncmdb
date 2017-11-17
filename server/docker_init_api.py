#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import DatabaseError
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .serializers import ServerContainerSerializers, ServerImageSerializers, ServerSerializers
from .models import ServerContainer, ServerImage, Server

import requests
import json
import time

class ListSwarmImage(APIView):

    def get_images(self):
        try:
            return ServerImage.objects.all()
        except ServerImage.DoesNotExist:
            raise DatabaseError

    def post(self, request, format=None):
        swarm_url = 'http://39.108.141.79:4000/images/json?all=1'
        headers = {'Content-Type': 'application/json'}
        r = requests.get(swarm_url, headers=headers)
        datas = r.json()
        # print datas
        for data in datas:
            x = time.localtime(data['Created'])
            created = time.strftime('%Y-%m-%d %H:%M:%S', x)
            y = int(data['Size'])/(1024*1024*8)
            image = {
                'Id': str(data['Id']).split(':')[1][:12],
                'Name': data['RepoTags'][0],
                'Created': created,
                'Size': str(y) + ' MB'
            }
            current_images = ServerImage.objects.filter(image_id=image['Id'])
            if current_images:
                current_images.update(image_id=image['Id'], image_name=image['Name'], size=image['Size'], createdate=image['Created'])
            else:
                current_images.create(image_id=image['Id'], image_name=image['Name'], size=image['Size'], createdate=image['Created'])

        images = self.get_images()
        serializer = ServerImageSerializers(images, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class DeletaSwarmImages(APIView):

    def post(self, request, format=None):
        # print json.loads(request.body)
        imageId = json.loads(request.body).get('image_id', None)
        if imageId is None:
            raise ParamException('image_id')
        dockerd_url = 'http://39.108.141.79:4000/images/%s' % imageId
        r = requests.delete(dockerd_url)
        code = r.status_code
        if code == '200' or code == 200 or code == '204' or code == 204:
            ServerImage.objects.filter(image_id=imageId).delete()
            response = {
                'retcode': 0,
                'retmsg': 'delete success'
            }
            return Response(response)
        else:
            raise Http404('image is not exist')


class InspectSwarmContain(APIView):

    def post(self, request, format=None):
        containerId = json.loads(request.body).get('container_id', None)
        if containerId is None:
            raise ParamException('container_id')
        dockerd_url = 'http://39.108.141.79:4000/containers/%s/top?ps_args=aux' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.get(dockerd_url, headers=headers)
        code = r.status_code
        data = r.json()
        payloads = []
        # print data
        if code == '200' or code == 200 or code == '204' or code == 204:
            for i in range(len(data['Processes'])):
                payload = {
                    'COMMAND': data['Processes'][i][-1],
                    'CPU': data['Processes'][i][2],
                    'MEM': data['Processes'][i][3],
                }
                payloads.append(payload)
            response = {
                'retcode': 0,
                'retdata': payloads,
            }
            return Response(response)
        else:
            raise Http404('container is not exist')

class ListSwarmContainer(APIView):

    def get_container(self):
        try:
            return ServerContainer.objects.all()
        except ServerContainer.DoesNotExist:
            raise DatabaseError

    def post(self, request, format=None):
        # containerId = json.loads(request.body).get('containerId', None)
        swarm_url = 'http://39.108.141.79:4000/containers/json?all=1'
        headers = {'Content-Type': 'application/json'}
        r = requests.get(swarm_url, headers=headers)
        datas = r.json()
        # print datas
        for data in datas:
            x = time.localtime(data['Created'])
            created = time.strftime('%Y-%m-%d %H:%M:%S', x)
            container = {
                'id': data['Id'][:12],
                'Name': data['Names'][0],
                'Host': str(data['Names'][0]).split('/')[1],
                'Image': data['Image'],
                'Command': data['Command'],
                'State': data['State'],
                'Status': data['Status'],
                'Created': created,
                }
            server = Server.objects.filter(name=container['Host'])
            serializer = ServerSerializers(server, many=True)
            server_id = serializer.data[0].get('id')
            # print server_id
            current_containers = ServerContainer.objects.filter(container_id=container['id'])
            if current_containers:
                current_containers.update(state=container['State'], status=container['Status'])
            else:
                current_containers.create(server_id=server_id, container_id=container['id'], container_name=container['Name'], image_name=container['Image'], \
                                            command=container['Command'], createdate=container['Created'], state=container['State'], status=container['Status'])
        containers = self.get_container()
        serializer = ServerContainerSerializers(containers, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)

class StopSwarmContain(APIView):

    def post(self, request, format=None):
        containerId = json.loads(request.body).get('container_id', None)
        if containerId is None:
            raise ParamException('container_id')
        dockerd_url = 'http://39.108.141.79:4000/containers/%s/stop' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.post(dockerd_url, headers=headers)
        code = r.status_code
        if code == '200' or code == 200 or code == '204' or code == 204:
            response = {
                'retcode': 0,
                'retmsg': 'stop success'
            }
            return Response(response)
        else:
            raise Http404('container is not exist')

class StartSwarmContain(APIView):

    def post(self, request, format=None):
        containerId = json.loads(request.body).get('container_id', None)
        if containerId is None:
            raise ParamException('container_id')
        dockerd_url = 'http://39.108.141.79:4000/containers/%s/start' % containerId
        headers = {'Content-Type': 'application/json'}
        r = requests.post(dockerd_url, headers=headers)
        code = r.status_code
        if code == '200' or code == 200 or code == '204' or code == 204:
            response = {
                'retcode': 0,
                'retmsg': 'start success'
            }
            return Response(response)
        else:
            raise Http404('container is not exist')

class DeleteSwarmContain(APIView):

    def post(self, request, format=None):
        containerId = json.loads(request.body).get('container_id', None)
        if containerId is None:
            raise ParamException('container_id')
        dockerd_url = 'http://39.108.141.79:4000/containers/%s' % containerId
        r = requests.delete(dockerd_url)
        code = r.status_code
        if code == '200' or code == 200 or code == '204' or code == 204:
            ServerContainer.objects.filter(container_id=containerId).delete()
            response = {
                'retcode': 0,
                'retmsg': 'delete success'
            }
            return Response(response)
        else:
            raise Http404('container is not exist')
