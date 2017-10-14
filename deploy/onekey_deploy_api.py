# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Records
# Create your views here.

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService', 'providerSystem', 'tempSystem', 'uco2Mobile', 'blackFaceWeb', 'blackfaceWap', 'blackfaceServer', 'blackfaceManage']
php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']

class PushTest(APIView):

    def create_record(self, record={}):
        try:
            Records.objects.create(project_name=record['project'], project_owner=record['project_owner'], \
                deploy_branch=record['deploy_branch'], deploy_tag=record['deploy_tag'], \
                project_type=record['type'], project_env=record['project_env'], deploy_status=record['status'], \
                commnet=record['comment'])
        except:
            raise DatabaseError

    def post(self, request, format=None):
        project = json.loads(request.body).get('project', None)
        branch = json.loads(request.body).get('branch', None)
        tag = json.loads(request.body).get('tag', None)

        test_host = 'web_test_1001'
        package_path = '/apps/packages/'
        tarfile_path = os.path.join(package_path, 'releases')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url_data = get_url(project)
        url = url_data['url']
        owner = url_data['owner']
        record = {
            'project_name': project,
            'project_owner': owner,
            'project_env': 'TEST',
            'deploy_branch': branch,
            'deploy_tag': tag
        }
        # reurl = str(url).replace('192.168.1.3', '112.74.182.80')
        dirname = project + '_test_' + branch + '_' + tag
        filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                arg = 'git checkout -b ' + branch + ' origin/' + branch
                checkout = os.popen(arg)
                # return HttpResponse(checkout.stdout)
            else:
                record['status'] = '失败'
                record['commnet'] = clone
                new_record = self.create_record(record)
                msg = {
                    'retcode': -1,
                    'retmsg': clone
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            lcd = os.chdir(package_path)
            # pwd = os.getcwd()
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()

        # 在master上打包
        if os.path.exists(project_dir):
            shutil.move(project_dir, project_dir + '_test_' + branch + '_' + tag)
            tag_dir = project_dir + '_test_' + branch + '_' + tag
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                # tar = 'tar -zcvf %s.tar.gz %s' % (filename, tag_dir)
                # os.popen(tar).readlines()
                msg = {
                    'retcode': 0,
                    'retmsg': 'tar dir success'
                }
                # return HttpResponse(json.dumps(msg))
            else:
                record['status'] = '失败'
                record['commnet'] = 'The project dir is not exists'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -2,
                    'retmsg': 'The project dir is not exists'
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            record['status'] = '失败'
            record['commnet'] = 'The filedir is not exists'
            new_record = self.create_record(record)
            msg = {
                'retcode': -2,
                'retmsg': 'The filedir is not exists'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 转移到master的上传目录复制到minions上
        # print tarfile_path + tarfilename
        # print os.path.exists(tarfile_path + '/' + tarfilename)
        if os.path.exists(tarfile_path + '/' + tarfilename):
            shutil.copyfile(tarfile_path + '/' + tarfilename, saltmaster_dir + tarfilename)
        else:
            record['status'] = '失败'
            record['commnet'] = 'copy error'
            new_record = self.create_record(record)
            msg = {
                'retcode': -3,
                'retmsg': 'copy error'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 使用saltapi上传文件并进行初始化
        if os.path.exists(saltmaster_dir + tarfilename):
            # saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
            saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
            src = 'salt://prod/packages/' + tarfilename
            dst = '/home/wwwroot/releases/' + tarfilename
            ft_rm = 'rm -rf /home/wwwroot/releases/' + filename
            rm_ft = saltapi.remote_execute(prod_host, 'cmd.run', ft_rm, 'glob')
            tar_rm = 'rm -rf /home/wwwroot/releases/' + tarfilename
            rm_tar = saltapi.remote_execute(prod_host, 'cmd.run', tar_rm, 'glob')
            upload = saltapi.file_copy(prod_host, 'cp.get_file', src, dst, 'glob')
            if upload:
                srv_arg = 'rm -rf ' + saltmaster_dir + tarfilename
                rm_srv = os.popen(srv_arg)
                # print rm_srv
                tar_arg = 'rm -rf ' + tarfile_path + '/' + tarfilename
                rm_tar = os.popen(tar_arg)
                # print rm_tar
                folder_arg = 'rm -rf ' + package_path + dirname
                rm_folder = os.popen(folder_arg)
                # print rm_folder
                mk = 'mkdir -p ' + '/home/wwwroot/releases/' + filename
                mkdir = saltapi.remote_execute(prod_host, 'cmd.run', mk, 'glob')
                tar = 'tar zxvf ' + dst + ' -C /home/wwwroot/releases/' + filename
                untar = saltapi.remote_execute(prod_host, 'cmd.run', tar, 'glob')
                rm = 'rm -rf /home/wwwroot/current/' + project
                remove = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                ln = 'ln -s /home/wwwroot/releases/' + filename + ' /home/wwwroot/current/' + project
                softlink = saltapi.remote_execute(prod_host, 'cmd.run', ln, 'glob')
                # update config and reload project
                if project in node_project_list:
                    rm, link = init_node_project_config(project, '/home/wwwroot/releases/' + filename, 'prod')
                    init = 'python /apps/sh/node_init.py %s init' % project
                    rm_run = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                    link_run = saltapi.remote_execute(prod_host, 'cmd.run', link, 'glob')
                    init_run = saltapi.remote_execute(prod_host, 'cmd.run', init, 'glob')
                    chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
                    chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')
                    # print init_run
                    record['type'] = 'node'
                    record['status'] = '成功'
                    record['commnet'] = project + ' 项目部署成功'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': 0,
                        'retmsg': project + ' 项目部署成功',
                    }
                    return Response(msg)
                elif project in php_project_list:
                    rm, rm_next, link, link_next = init_php_project_config(project, '/home/wwwroot/releases/' + filename, 'prod')
                    rm_run = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                    rm_next_run = saltapi.remote_execute(prod_host, 'cmd.run', rm_next, 'glob')
                    link_run = saltapi.remote_execute(prod_host, 'cmd.run', link, 'glob')
                    link_next_run = saltapi.remote_execute(prod_host, 'cmd.run', link_next, 'glob')
                    chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
                    chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')

                    record['type'] = 'php'
                    record['status'] = '成功'
                    record['commnet'] = project + ' 项目部署成功'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': 0,
                        'retmsg': project + ' 项目部署成功',
                    }
                    return Response(msg)
                else:
                    record['status'] = '失败'
                    record['commnet'] = 'current path is not exist'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': -4,
                        'retmsg': 'current path is not exist'
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                record['status'] = '失败'
                record['commnet'] = 'upload failed'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -5,
                    'retmsg': 'upload failed'
                }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            record['status'] = '失败'
            record['commnet'] = 'saltfile error'
            new_record = self.create_record(record)
            msg = {
                'retcode': -5,
                'retmsg': 'saltfile error'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PushProd(APIView):

    def create_record(self, record={}):
        try:
            Records.objects.create(project_name=record['project'], project_owner=record['project_owner'], \
                deploy_branch=record['deploy_branch'], deploy_tag=record['deploy_tag'], \
                project_type=record['type'], project_env=record['project_env'], deploy_status=record['status'], \
                commnet=record['comment'])
        except:
            raise DatabaseError

    def post(self, request, format=None):
        project = json.loads(request.body).get('project', None)
        branch = json.loads(request.body).get('branch', None)
        tag = json.loads(request.body).get('tag', None)

        test_host = 'web_prod_1001'
        package_path = '/apps/packages/'
        tarfile_path = os.path.join(package_path, 'releases')
        project_dir = os.path.join(package_path, project)
        saltmaster_dir = '/srv/salt/test/packages/'

        url_data = get_url(project)
        url = url_data['url']
        owner = url_data['owner']
        record = {
            'project_name': project,
            'project_owner': owner,
            'project_env': 'PROD',
            'deploy_branch': branch,
            'deploy_tag': tag
        }
        dirname = project + '_prod_' + branch + '_' + tag
        filename = project + '_prod_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
        tarfilename = project + '_prod_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
        # 先在master上处理git操作
        if branch != 'master':
            lcd = os.chdir(package_path)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                arg = 'git checkout -b ' + branch + ' origin/' + branch
                checkout = os.popen(arg)
                # return HttpResponse(checkout.stdout)
            else:
                record['status'] = '失败'
                record['commnet'] = clone
                new_record = self.create_record(record)
                msg = {
                    'retcode': -1,
                    'retmsg': clone
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            lcd = os.chdir(package_path)
            # pwd = os.getcwd()
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            # print clone

        # print os.listdir(package_path)
        # print os.path.exists(project_dir)
        # 在master上打包
        if os.path.exists(project_dir):
            shutil.move(project_dir, project_dir + '_prod_' + branch + '_' + tag)
            tag_dir = project_dir + '_prod_' + branch + '_' + tag
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': '0',
                    'retmsg': 'tar dir success'
                }
                # return HttpResponse(json.dumps(msg))
            else:
                record['status'] = '失败'
                record['commnet'] = 'The project dir is not exists'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -2,
                    'retmsg': 'The project dir is not exists'
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            record['status'] = '失败'
            record['commnet'] = 'The filedir is not exists'
            new_record = self.create_record(record)
            msg = {
                'retcode': -2,
                'retmsg': 'The filedir is not exists'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 转移到master的上传目录复制到minions上
        print tarfile_path + tarfilename
        print os.path.exists(tarfile_path + '/' + tarfilename)
        if os.path.exists(tarfile_path + '/' + tarfilename):
            shutil.copyfile(tarfile_path + '/' + tarfilename, saltmaster_dir + tarfilename)
        else:
            msg = 'copy error'
            return HttpResponseServerError(json.dumps(msg))

        # 使用saltapi上传文件并进行初始化
        if os.path.exists(saltmaster_dir + tarfilename):
            # saltapi = SaltAPI('https://112.74.164.242:7000', 'saltapi', 'saltadmin')
            saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
            src = 'salt://prod/packages/' + tarfilename
            dst = '/home/wwwroot/releases/' + tarfilename
            ft_rm = 'rm -rf /home/wwwroot/releases/' + filename
            rm_ft = saltapi.remote_execute(prod_host, 'cmd.run', ft_rm, 'glob')
            tar_rm = 'rm -rf /home/wwwroot/releases/' + tarfilename
            rm_tar = saltapi.remote_execute(prod_host, 'cmd.run', tar_rm, 'glob')
            upload = saltapi.file_copy(prod_host, 'cp.get_file', src, dst, 'glob')
            if upload:
                srv_arg = 'rm -rf ' + saltmaster_dir + tarfilename
                rm_srv = os.popen(srv_arg)
                # print rm_srv
                tar_arg = 'rm -rf ' + tarfile_path + '/' + tarfilename
                rm_tar = os.popen(tar_arg)
                # print rm_tar
                folder_arg = 'rm -rf ' + package_path + dirname
                rm_folder = os.popen(folder_arg)
                # print rm_folder
                mk = 'mkdir -p ' + '/home/wwwroot/releases/' + filename
                mkdir = saltapi.remote_execute(prod_host, 'cmd.run', mk, 'glob')
                tar = 'tar zxvf ' + dst + ' -C /home/wwwroot/releases/' + filename
                untar = saltapi.remote_execute(prod_host, 'cmd.run', tar, 'glob')
                rm = 'rm -rf /home/wwwroot/current/' + project
                remove = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                ln = 'ln -s /home/wwwroot/releases/' + filename + ' /home/wwwroot/current/' + project
                softlink = saltapi.remote_execute(prod_host, 'cmd.run', ln, 'glob')
                # update config and reload project
                if project in node_project_list:
                    rm, link = init_node_project_config(project, '/home/wwwroot/releases/' + filename, 'prod')
                    init = 'python /apps/sh/node_init.py %s init' % project
                    rm_run = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                    link_run = saltapi.remote_execute(prod_host, 'cmd.run', link, 'glob')
                    init_run = saltapi.remote_execute(prod_host, 'cmd.run', init, 'glob')
                    chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
                    chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')
                    # print init_run
                    record['type'] = 'node'
                    record['status'] = '成功'
                    record['commnet'] = project + ' 项目部署成功'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': 0,
                        'retmsg': project + ' 项目部署成功',
                    }
                    return Response(msg)
                elif project in php_project_list:
                    rm, rm_next, link, link_next = init_php_project_config(project, '/home/wwwroot/releases/' + filename, 'prod')
                    rm_run = saltapi.remote_execute(prod_host, 'cmd.run', rm, 'glob')
                    rm_next_run = saltapi.remote_execute(prod_host, 'cmd.run', rm_next, 'glob')
                    link_run = saltapi.remote_execute(prod_host, 'cmd.run', link, 'glob')
                    link_next_run = saltapi.remote_execute(prod_host, 'cmd.run', link_next, 'glob')
                    chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
                    chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')

                    record['type'] = 'php'
                    record['status'] = '成功'
                    record['commnet'] = project + ' 项目部署成功'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': 0,
                        'retmsg': project + ' 项目部署成功',
                    }
                    return Response(msg)
                else:
                    record['status'] = '失败'
                    record['commnet'] = 'current path is not exist'
                    new_record = self.create_record(record)
                    msg = {
                        'retcode': -4,
                        'retmsg': 'current path is not exist'
                    }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                record['status'] = '失败'
                record['commnet'] = 'upload failed'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -5,
                    'retmsg': 'upload failed'
                }
                return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            record['status'] = '失败'
            record['commnet'] = 'saltfile error'
            new_record = self.create_record(record)
            msg = {
                'retcode': -5,
                'retmsg': 'saltfile error'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def init_php_project_config(project, path, env):
    # php_project_list = ['beeHive', 'uco2H5', 'kalachakraMS']
    if project in php_project_list:
        if env == 'test':
            test_path = path + '/Global/config.test.js'
            cur_path = path + '/Global/config.js'
            test_path_next = path + '/Interface/application/config.test.php'
            cur_path_next = path + '/Interface/application/config.php'
            rm = 'rm -f ' + cur_path
            rm_next = 'rm -f ' + cur_path_next
            link = 'ln -s ' + test_path + ' ' + cur_path
            link_next = 'ln -s ' + test_path_next + ' ' + cur_path_next
            return rm, rm_next, link, link_next
        elif env == 'prod':
            prod_path = path + '/Global/config.prod.js'
            cur_path = path + '/Global/config.js'
            prod_path_next = path + '/Interface/application/config.prod.php'
            cur_path_next = path + '/Interface/application/config.php'
            rm = 'rm -f ' + cur_path
            rm_next = 'rm -f ' + cur_path_next
            link = 'ln -s ' + prod_path + ' ' + cur_path
            link_next = 'ln -s ' + prod_path_next + ' ' + cur_path_next
            return rm, rm_next, link, link_next
        else:
            msg = {
                'retcode': -1
                }
            return msg
    else:
        msg = {
            'retcode': 1
        }
        return msg

def init_node_project_config(project, path, env):
    # node_project_list = ['platformService', 'uco2Web', 'gdrManagerSystem', 'uco2Notice', 'YoungBody', 'kalachakraWeb', 'kalachakraService']
    if project in node_project_list:
        if env == 'test':
            test_path = path + '/global/config.test.js'
            cur_path = path + '/global/config.js'
            rm = 'rm -f ' + cur_path
            link = 'ln -s ' + test_path + ' ' + cur_path
            return rm, link
        elif env == 'prod':
            prod_path = path + '/global/config.prod.js'
            cur_path = path + '/global/config.js'
            rm = 'rm -f ' + cur_path
            link = 'ln -s ' + prod_path + ' ' + cur_path
            return rm, link
        else:
            msg = {
                'retcode': -1
            }
            return msg
    else:
        msg = {
            'retcode': 1
        }
        return msg
