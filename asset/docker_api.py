#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Docker_Container, Docker_Image
from .serializers import DockerContainerSerializers, DockerImageSerializers

import requests
import json
import time

class ContainerList(APIView):

    def get(self, request, format=None):
        containers = Docker_Container.objects.all()
        serializer = DockerContainerSerializers(containers, many=True)
        return Response(serializer.data)

class ImageList(APIView):

    def get(self, request, format=None):
        images = Docker_Image.objects.all()
        serializer = DockerImageSerializers(images, many=True)
        return Response(serializer.data)

class ContainerDetail(APIView):

    def get_object(self, requests, pk):
        try:
            return Docker_Container.objects.get(containerId=pk)
        except Server.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        container = self.get_object(pk)
        serializer = DockerContainerSerializers(container)
        return Response(serializer.data)
