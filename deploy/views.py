# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
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
        tarfile_path = os.path.join(package_path, 'release')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url = get_url_api(project)
        dirname = project + '_test_' + branch + '_' + tag
        filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            arg = 'git clone ' + url
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
            pwd = os.getcwd()
            print pwd
            arg = 'git clone ' + url
            print arg
            clone = os.popen(arg)
        # 在master上打包
        if os.path.exists(project_dir):
            tag_dir = shutil.move(project_dir, project_dir + '_test_' + branch + '_' + tag)
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "tar.gz", root_dir=project_dir)
            else:
                msg = {
                    'retcode': '-1',
                    'retmsg': 'The project dir is not exists'
                    }
                return HttpResponse(json.dumps(msg))
        else:
            msg = {
                'retcode': '-2',
                'retmsg': 'The filedir is not exists'
            }
            return HttpResponse(json.dumps(msg))

        # 转移到master的上传目录复制到minions上
        if os.path.exists(tarfile_path + filename):
            shutil.copyfile(tarfile_path + filename, saltmaster_dir + filename)
        else:
            msg = 'copy error'
            return HttpResponse(msg)

        # 使用saltapi上传文件
        saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
        src = 'salt://test/packages/' + filename
        dst = '/home/wwwroot/release/' + filename
        upload = saltapi.file_copy(test_host, 'cp.get_file', src, dst)
        return HttpResponse(upload)
