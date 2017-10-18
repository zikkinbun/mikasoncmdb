# coding: utf-8
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .models import Server, IDC
from .serializers import ServerSerializers
import json
# Create your views here.

class ListServer(APIView):
    """
        list all servers or create a server
    """

    def post(self, request, format=None):
        servers = Server.objects.all()
        serializer = ServerSerializers(servers, many=True)
        # print serializer.data
        data = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(data)


class CreateServer(APIView):

    def post(self, request, format=None):
        serializer = ServerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'retcode': 0,
                'retdata': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getServerDetail(APIView):

    def get_object(self, pk):
        try:
            return Server.objects.get(id=pk)
        except Server.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = json.loads(request.body).get('id', None)
        if pk is None:
            raise ParamException('id')
        server = self.get_object(pk)
        serializer = ServerSerializers(server)
        data = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(data)


class EditServerDetail(APIView):
    """
        look up the detail server or update a sevser
    """

    def get_object(self, pk):
        try:
            return Server.objects.get(id=pk)
        except Server.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = json.loads(request.body).get('id', None)
        if pk is None:
            raise ParamException('id')
        server = self.get_object(pk)
        serializer = ServerSerializers(server, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteServer(APIView):
    """
        delete a server
    """

    def get_object(self, pk):
        try:
            return Server.objects.get(id=pk)
        except Server.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        pk = json.loads(request.body).get('id', None)
        if pk is None:
            raise ParamException('id')
        server = self.get_object(pk)
        server.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
