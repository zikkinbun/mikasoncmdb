# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

@csrf_exempt
def pushTest(request):
    if request.POST:
        project = json.loads(request.body)[u'project']
        branch = json.loads(request.body)[u'branch']
        tag = json.loads(request.body)[u'tag']
        # project = request.POST.get('project', '')
        # branch = request.POST.get('branch', '')
        # tag = request.POST.get('tag', '')

        test_host = 'web_test_1001'
        package_path = '/apps/packages/'
        tarfile_path = os.path.join(package_path, 'releases')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url = get_url_api(project)
        reurl = str(url).replace('192.168.1.3', '112.74.182.80')
        dirname = project + '_test_' + branch + '_' + tag
        filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            arg = 'git clone ' + reurl
            clone = subprocess.Popen(arg)
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                arg = 'git checkout -b ' + branch + ' origin/' + branch
                checkout = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
                return HttpResponse(checkout.stdout)
            else:
                msg = clone.stdout
                return HttpResponse(msg)
        else:
            lcd = os.chdir(package_path)
            # pwd = os.getcwd()
            arg = 'git clone ' + reurl
            clone = os.popen(arg).readlines()
            # print clone

        # print os.listdir(package_path)
        # print os.path.exists(project_dir)
        # 在master上打包
        if os.path.exists(project_dir):
            shutil.move(project_dir, project_dir + '_test_' + branch + '_' + tag)
            tag_dir = project_dir + '_test_' + branch + '_' + tag
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': '0',
                    'retmsg': 'tar dir success'
                }
                # return HttpResponse(json.dumps(msg))
            else:
                msg = {
                    'retcode': '-1',
                    'retmsg': 'The project dir is not exists'
                    }
                return HttpResponseServerError(json.dumps(msg))
        else:
            msg = {
                'retcode': '-2',
                'retmsg': 'The filedir is not exists'
            }
            return HttpResponseServerError(json.dumps(msg))

        # 转移到master的上传目录复制到minions上
        # print tarfile_path + tarfilename
        # print os.path.exists(tarfile_path + '/' + tarfilename)
        if os.path.exists(tarfile_path + '/' + tarfilename):
            shutil.copyfile(tarfile_path + '/' + tarfilename, saltmaster_dir + tarfilename)
        else:
            msg = 'copy error'
            return HttpResponseServerError(msg)

        # 使用saltapi上传文件
        if os.path.exists(saltmaster_dir + tarfilename):
            saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
            src = 'salt://test/packages/' + filename
            dst = '/home/wwwroot/release/' + filename
            upload = saltapi.file_copy(test_host, 'cp.get_file', src, dst)
            return HttpResponse(upload)
        else:
            msg = 'saltfile error'
            return HttpResponseServerError(msg)
