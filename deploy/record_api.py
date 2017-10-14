# coding: utf-8
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Records
from .serializers import RecordsSerializers

import json

class GetRecords(APIView):

    def get_record_all(self):
        try:
            return Records.objects.all()
        except:
            raise DatabaseError

    def post(self, request, format=None):

        record = self.get_record_all()
        serializer = RecordsSerializers(record, many=True)
        response = {
            'retcode': 0,
            'retdata': serializer.data
        }
        return Response(response)
