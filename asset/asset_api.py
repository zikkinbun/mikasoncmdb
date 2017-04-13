# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Server, IDC
from .serializers import ServerSerializers
import json
# Create your views here.

# class ServerListViewSet(viewsets.ModelViewSet):
#     serializer_class = ServerSerializers
#     queryset = Server.objects.all()
#
#     def list(self, request):
#         servers = Server.objects.all()
#         page = self.paginate_queryset(servers)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(servers, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
# class ServerDetailViewSet(viewsets.ModelViewSet):
#     serializer_class = ServerSerializers
#     queryset = Server.objects.all()
#
#     def update(self, request, pk):
#         server = Server.objects.filter(Id=pk)
#         # serializer = ServerSerializers(data=request.data)
#         serializer = self.get_serializer(server, data=request.data)
#         if serializer.is_valid():
#             server.update(Name=serializer.data['Name'])
#             server.update(System=serializer.data['System'])
#             server.update(GlobalIpAddr=serializer.data['GlobalIpAddr'])
#             server.update(PrivateIpAddr=serializer.data['PrivateIpAddr'])
#             server.update(CpuStat=serializer.data['CpuStat'])
#             server.update(MemoryStat=serializer.data['MemoryStat'])
#             server.update(HDDStorage=serializer.data['HDDStorage'])
#             server.update(NetCard=serializer.data['NetCard'])
#             server.update(Status=serializer.data['Status'])
#             server.update(comment=serializer.data['comment'])
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         # print pk
#         server = Server.objects.filter(id=pk)
#         server.delete()
#         return Response("{'msg': '已删除'}")

class ServerList(APIView):
    """
        list all servers or create a server
    """

    def get(self, request, format=None):
        servers = Server.objects.all()
        serializer = ServerSerializers(servers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer.ServerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
