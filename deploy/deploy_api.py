#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Records
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

class Deploy(APIView):

    def create_record(self, record):
        try:
            print record
            return Records.objects.create(project_name=record['project_name'], project_owner=record['project_owner'], \
                deploy_branch=record['deploy_branch'], deploy_tag=record['deploy_tag'], \
                project_type=record['project_type'], project_env=record['project_env'], deploy_status=record['status'], \
                comment=record['comment'])
        except Exception as e:
            print e

    def reset_configfile(self, path, configfiles, env):
        cmds = []
        for configfile in configfiles:
            config = str(configfile).split('/')
            _config = config.pop(-1).replace('config', 'config.%s' % env)
            config.append(_config)
            _configfile = '/'.join(config)
            ln_cmd = 'ln -s ' + path + _configfile + ' ' + path + configfile
            rm_cmd = 'rm -f ' + path + configfile
            cmds.append(rm_cmd)
            cmds.append(ln_cmd)

        return cmds

    def clone_checkout(self, record, url, package_dir, project_dir):
        if record['deploy_branch'] != 'master':
            lcd = os.chdir(package_dir)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            if os.path.exists(project_dir):
                os.chdir(project_dir)
                arg = 'git checkout -b ' + record['deploy_branch'] + ' origin/' + record['deploy_branch']
                checkout = os.popen(arg)
                msg = {
                    'retcode': 0,
                    'retmsg': 'success'
                    }
                return msg
            else:
                record['status'] = '失败'
                record['commnet'] = clone
                new_record = self.create_record(record)
                msg = {
                    'retcode': -1,
                    'retmsg': clone
                    }
                return msg
        else:
            lcd = os.chdir(package_dir)
            arg = 'git clone ' + url
            clone = os.popen(arg).readlines()
            msg = {
                'retcode': 0,
                'retmsg': 'success'
                }
            return msg

    def tar_package(self, record, project_dir, tarfile_path, filename, env):
        if os.path.exists(project_dir):
            shutil.move(project_dir, project_dir + '_' + env +'_' + record['deploy_branch'] + '_' + record['deploy_tag'])
            tag_dir = project_dir + '_prod_' + record['deploy_branch'] + '_' + record['deploy_tag']
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': '0',
                    'retmsg': 'tar dir success'
                }
                return msg
            else:

                record['status'] = u'失败'
                record['commnet'] = 'The project dir is not exists'
                print record
                new_record = self.create_record(record)
                msg = {
                    'retcode': -2,
                    'retmsg': 'The project dir is not exists'
                    }
                return msg
        else:

            record['status'] = '失败'
            record['commnet'] = 'The filedir is not exists'
            new_record = self.create_record(record)
            msg = {
                'retcode': -2,
                'retmsg': 'The filedir is not exists'
            }
            return msg

    def cp_saltdir(self, record, tarfile_path, tarfilename, saltmaster_dir):
        if os.path.exists(tarfile_path + '/' + tarfilename):
            shutil.copyfile(tarfile_path + '/' + tarfilename, saltmaster_dir + tarfilename)
            msg = {
                'retcode': 0,
                'retmsg': 'success'
                }
            return msg
        else:
            record['status'] = '失败'
            record['commnet'] = 'copy error'
            new_record = self.create_record(record)
            msg = {
                'retcode': -1,
                'retmsg': 'copy error'
            }
            return msg

    def saltApi_copy_dst(self, record, target, saltmaster_dir, tarfilename, filename, env):
        if os.path.exists(saltmaster_dir + tarfilename):
            saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
            src = 'salt://' + env + '/packages/' + tarfilename
            dst = '/home/wwwroot/releases/' + tarfilename
            ft_rm = 'rm -rf /home/wwwroot/releases/' + filename
            rm_ft = saltapi.remote_execute(target, 'cmd.run', ft_rm, 'glob')
            tar_rm = 'rm -rf /home/wwwroot/releases/' + tarfilename
            rm_tar = saltapi.remote_execute(target, 'cmd.run', tar_rm, 'glob')
            upload = saltapi.file_copy(target, 'cp.get_file', src, dst, 'glob')
            if upload:
                msg = {
                    'retcode': 0,
                    'retmsg': 'upload success'
                    }
                return msg
            else:
                record['status'] = '失败'
                record['commnet'] = 'upload failed'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -1,
                    'retmsg': 'upload failed'
                }
                return msg
        else:
            record['status'] = '失败'
            record['commnet'] = 'The salt tar dir is not exists'
            new_record = self.create_record(record)
            msg = {
                'retcode': -2,
                'retmsg': 'The salt tar dir is not exists'
            }
            return msg

    def saltApi_release_dir(self, record, target, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename):
        saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
        srv_arg = 'rm -rf ' + saltmaster_dir + tarfilename
        rm_srv = os.popen(srv_arg)
        tar_arg = 'rm -rf ' + tarfile_path + '/' + tarfilename
        rm_tar = os.popen(tar_arg)
        folder_arg = 'rm -rf ' + package_path + dirname
        rm_folder = os.popen(folder_arg)
        mk = 'mkdir -p ' + '/home/wwwroot/releases/' + filename
        mkdir = saltapi.remote_execute(target, 'cmd.run', mk, 'glob')
        tar = 'tar zxvf ' + '/home/wwwroot/releases/' + tarfilename + ' -C /home/wwwroot/releases/' + filename
        untar = saltapi.remote_execute(target, 'cmd.run', tar, 'glob')
        rm = 'rm -rf /home/wwwroot/current/' + record['project_name']
        remove = saltapi.remote_execute(target, 'cmd.run', rm, 'glob')
        ln = 'ln -s /home/wwwroot/releases/' + filename + ' /home/wwwroot/current/' + record['project_name']
        softlink = saltapi.remote_execute(target, 'cmd.run', ln, 'glob')
        if softlink:
            msg = {
                'retcode': 0,
                'retmsg': 'success'
            }
            return msg
        else:
            record['status'] = '失败'
            record['commnet'] = 'fail to release'
            new_record = self.create_record(record)
            msg = {
                'retcode': -1,
                'retmsg': 'fail to release'
            }
            return msg

    def saltApi_config_dir(self, cmds, target, record):
        saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
        init = 'python /apps/sh/node_init.py %s init' % project
        # chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
        for cmd in cmds:
            saltapi.remote_execute(target, 'cmd.run', cmd, 'glob')
        init_run = saltapi.remote_execute(target, 'cmd.run', init, 'glob')
        # chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')

        record['type'] = 'node'
        record['status'] = '成功'
        record['commnet'] = project + ' 项目部署成功'
        new_record = self.create_record(record)
        msg = {
            'retcode': 0,
            'retmsg': project + ' 项目部署成功',
        }
        return msg

    def post(self, request, format=None):
        project = json.loads(request.body).get('project', None)
        if project is None:
            raise ParamException('project')
        branch = json.loads(request.body).get('branch', None)
        if branch is None:
            raise ParamException('branch')
        tag = json.loads(request.body).get('tag', None)
        if tag is None:
            raise ParamException('tag')
        env = json.loads(request.body).get('env', None)
        if env is None:
            raise ParamException('env')
        configfile = json.loads(request.body).get('configfile', None)
        if configfile is None:
            raise ParamException('configfile')
        type = json.loads(request.body).get('project_type', None)
        if type is None:
            raise ParamException('project_type')

        if env == 'test':
            test_host = 'web_test_1001'
            package_path = '/apps/packages/'
            tarfile_path = os.path.join(package_path, 'releases')
            project_dir = os.path.join(package_path, project)
            saltmaster_dir = '/srv/salt/test/packages/'

            url_data = get_url(project)
            url = url_data['url']
            owner = url_data['owner']

            dirname = project + '_test_' + branch + '_' + tag
            filename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
            tarfilename = project + '_test_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
            record = {
                'project_name': project,
                'project_owner': owner,
                'project_env': 'TEST',
                'project_type': type,
                'deploy_branch': branch,
                'deploy_tag': tag
            }

            cmds = self.reset_configfile('/home/wwwroot/releases/', configfile, env)
            checkout = self.clone_checkout(record, url, package_path, project_dir)
            if checkout['retcode'] == 0:
                tar = self.tar_package(record, project_dir, tarfile_path, filename, env)
                if tar['retcode'] == 0:
                    cp = self.cp_saltdir(record, tarfile_path, tarfilename, saltmaster_dir)
                    if cp['retcode'] == 0:
                        upload = self.saltApi_copy_dst(record, test_host, saltmaster_dir, tarfilename, filename, env)
                        if upload['retcode'] == 0:
                            release = self.saltApi_release_dir(record, test_host, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename)
                            if release['retcode'] == 0:
                                config = self.saltApi_config_dir(cmds, test_host, record)
                                if config['retcode'] == 0:
                                    return Response(config)
                                else:
                                    return Response(config, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            else:
                                return Response(release, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response(upload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response(cp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(tar, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(checkout, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif env == 'prod':
            prod_host = 'web_prod_1001'
            package_path = '/apps/packages/'
            tarfile_path = os.path.join(package_path, 'releases')
            project_dir = os.path.join(package_path, project)
            saltmaster_dir = '/srv/salt/prod/packages/'

            url_data = get_url(project)
            url = url_data['url']
            owner = url_data['owner']

            dirname = project + '_prod_' + branch + '_' + tag
            filename = project + '_prod_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d")
            tarfilename = project + '_prod_' + branch + '_' + tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
            record = {
                'project_name': project,
                'project_owner': owner,
                'project_env': 'PROD',
                'deploy_branch': branch,
                'deploy_tag': tag
            }

            cmds = self.reset_configfile('/home/wwwroot/releases/', configfile, env)
            checkout = self.clone_checkout(record, url, package_path, project_dir)
            if checkout['retcode'] == 0:
                tar = self.tar_package(record, project_dir, tarfile_path, filename, env)
                if tar['retcode'] == 0:
                    cp = self.cp_saltdir(record, tarfile_path, tarfilename, saltmaster_dir)
                    if cp['retcode'] == 0:
                        upload = self.saltApi_copy_dst(record, prod_host, saltmaster_dir, tarfilename, filename, env)
                        if upload['retcode'] == 0:
                            release = self.saltApi_release_dir(record, prod_host, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename)
                            if release['retcode'] == 0:
                                config = self.saltApi_config_dir(cmds, prod_host, record)
                                if config['retcode'] == 0:
                                    return Response(config)
                                else:
                                    return Response(config, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            else:
                                return Response(release, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response(upload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response(cp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(tar, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(checkout, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            msg = {
                'retcode': -3,
                'retmsg': 'ENV is not setted'
            }
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
