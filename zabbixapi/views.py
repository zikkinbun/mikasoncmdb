# _*_ coding:utf-8_*_
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json

from .models import cpuload, cpustat, memstat
# Create your views here.

@csrf_exempt
def getCPUSTAT(request):
    if request.method == 'GET':
        current_data = cpustat.objects.all().limit(10)
