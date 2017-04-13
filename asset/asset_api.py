# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Server, IDC
from .serializers import ServerSerializers
import json
# Create your views here.

class ServerList(APIView):
    """
        list all servers or create a server
    """

    def get(self, request, format=None):
        servers = Server.objects.all()
        serializer = ServerSerializers(servers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ServerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerDetail(APIView):
    """
        look up the detail server or update a sevser
    """

    def get_object(self, pk):
        try:
            return Server.objects.get(id=pk)
        except Server.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = ServerSerializers(server)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        # print request.data
        server = self.get_object(pk)
        serializer = ServerSerializers(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerDelete(APIView):
    """
        delete a server
    """

    def get_object(self, pk):
        try:
            return Server.objects.get(id=pk)
        except Server.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        server = self.get_object(pk)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
