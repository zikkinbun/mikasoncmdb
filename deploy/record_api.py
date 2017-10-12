# coding: utf-8
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Records
from .serializers import RecordsSerializers

import json
