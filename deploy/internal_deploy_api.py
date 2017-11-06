# coding: utf-8
from django.db import DatabaseError
from .models import Records
# Create your views here.

from .gitlab_api import *
from .salt_api import *

import time
import subprocess
import shutil
import json
import os

class PeriodDeploy(object):

    def __init__(self, project, branch, tag, config, type, env=None, target=None):
        self.project = project
        self.branch = branch
        self.tag = tag
        self.env = env
        self.target = target
        self.config = []
        self.config.append(config)
        self.type = type

    def create_record(self, record):
        try:
            # print record
            return Records.objects.create(project_name=record['project_name'], project_owner=record['project_owner'], \
                deploy_branch=record['deploy_branch'], deploy_tag=record['deploy_tag'], \
                project_type=record['project_type'], project_env=record['project_env'], deploy_status=record['status'], \
                comment=record['comment'])
        except:
            raise DatabaseError

    def reset_configfile(self, filename, path, configfiles, env):
        cmds = []
        # print configfiles
        for configfile in configfiles:
            # print configfile
            config = str(configfile).split('/')
            # print config
            _config = config.pop(-1)
            # print _config
            env_config = _config.replace('config', 'config.%s' % env)
            # print env_config
            config.append(env_config)
            # print config
            _configfile = '/'.join(config)
            ln_cmd = 'ln -s ' + path + filename + _configfile + ' ' + path + filename + configfile
            rm_cmd = 'rm -f ' + path + filename + configfile
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
                record['comment'] = clone
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
            tag_dir = project_dir + '_' + env + '_' + record['deploy_branch'] + '_' + record['deploy_tag']
            # print tag_dir
            # print os.path.exists(tag_dir)
            if os.path.exists(tag_dir):
                os.chdir(tarfile_path)
                shutil.make_archive(filename, "gztar", root_dir=tag_dir)
                msg = {
                    'retcode': 0,
                    'retmsg': 'tar dir success'
                }
                return msg
            else:
                record['status'] = u'失败'
                record['comment'] = 'The project dir is not exists'
                # print record
                new_record = self.create_record(record)
                msg = {
                    'retcode': -2,
                    'retmsg': 'The project dir is not exists'
                    }
                return msg
        else:
            record['status'] = '失败'
            record['comment'] = 'The filedir is not exists'
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
            record['comment'] = 'copy error'
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
                record['comment'] = 'upload failed'
                new_record = self.create_record(record)
                msg = {
                    'retcode': -1,
                    'retmsg': 'upload failed'
                }
                return msg
        else:
            record['status'] = '失败'
            record['comment'] = 'The salt tar dir is not exists'
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
            record['comment'] = 'fail to release'
            new_record = self.create_record(record)
            msg = {
                'retcode': -1,
                'retmsg': 'fail to release'
            }
            return msg

    def saltApi_config_dir(self, cmds, target, record):
        saltapi = SaltAPI('https://120.77.46.79:7000', 'saltapi', 'saltadmin')
        init = 'python /apps/sh/node_init.py %s init' % record['project_name']
        # chown = 'chown -R prod.prod /home/wwwroot/releases/' + filename
        print cmds
        for cmd in cmds:
            saltapi.remote_execute(target, 'cmd.run', cmd, 'glob')
        init_run = saltapi.remote_execute(target, 'cmd.run', init, 'glob')
        # chown_run = saltapi.remote_execute(prod_host, 'cmd.run', chown, 'glob')

        record['type'] = 'node'
        record['status'] = '成功'
        record['comment'] = record['project_name'] + u' 项目定时部署成功'
        new_record = self.create_record(record)
        msg = {
            'retcode': 0,
            'retmsg': record['project_name'] + u' 项目定时部署成功',
        }
        return msg

    def run(self):

        if self.env == 'test':
            test_host = 'web_test_1001'
            package_path = '/apps/packages/'
            tarfile_path = os.path.join(package_path, 'releases')
            project_dir = os.path.join(package_path, self.project)
            saltmaster_dir = '/srv/salt/test/packages/'

            url_data = get_url(self.project)
            url = url_data['url']
            owner = url_data['owner']

            dirname = self.project + '_test_' + self.branch + '_' + self.tag
            filename = self.project + '_test_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d")
            tarfilename = self.project + '_test_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
            record = {
                'project_name': self.project,
                'project_owner': owner,
                'project_env': 'TEST',
                'project_type': self.type,
                'deploy_branch': self.branch,
                'deploy_tag': self.tag
            }

            cmds = self.reset_configfile(filename, '/home/wwwroot/releases/', self.config, self.env)
            # print cmds
            checkout = self.clone_checkout(record, url, package_path, project_dir)
            if checkout['retcode'] == 0:
                tar = self.tar_package(record, project_dir, tarfile_path, filename, self.env)
                if tar['retcode'] == 0:
                    cp = self.cp_saltdir(record, tarfile_path, tarfilename, saltmaster_dir)
                    if cp['retcode'] == 0:
                        upload = self.saltApi_copy_dst(record, test_host, saltmaster_dir, tarfilename, filename, self.env)
                        if upload['retcode'] == 0:
                            release = self.saltApi_release_dir(record, test_host, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename)
                            if release['retcode'] == 0:
                                config = self.saltApi_config_dir(cmds, test_host, record)
                                return config
                            else:
                                return release
                        else:
                            return upload
                    else:
                        return cp
                else:
                    return tar
            else:
                return checkout
        elif self.env == 'prod':
            prod_host = 'web_prod_1001'
            package_path = '/apps/packages/'
            tarfile_path = os.path.join(package_path, 'releases')
            project_dir = os.path.join(package_path, self.project)
            saltmaster_dir = '/srv/salt/prod/packages/'

            url_data = get_url(self.project)
            url = url_data['url']
            owner = url_data['owner']

            dirname = self.project + '_prod_' + self.branch + '_' + self.tag
            filename = self.project + '_prod_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d")
            tarfilename = self.project + '_prod_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
            record = {
                'project_name': self.project,
                'project_owner': owner,
                'project_env': 'PROD',
                'project_type': self.type,
                'deploy_branch': self.branch,
                'deploy_tag': self.tag
            }

            cmds = self.reset_configfile(filename, '/home/wwwroot/releases/', self.config, self.env)
            checkout = self.clone_checkout(record, url, package_path, project_dir)
            if checkout['retcode'] == 0:
                tar = self.tar_package(record, project_dir, tarfile_path, filename, self.env)
                if tar['retcode'] == 0:
                    cp = self.cp_saltdir(record, tarfile_path, tarfilename, saltmaster_dir)
                    if cp['retcode'] == 0:
                        upload = self.saltApi_copy_dst(record, prod_host, saltmaster_dir, tarfilename, filename, self.env)
                        if upload['retcode'] == 0:
                            release = self.saltApi_release_dir(record, prod_host, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename)
                            if release['retcode'] == 0:
                                config = self.saltApi_config_dir(cmds, prod_host, record)
                                return config
                            else:
                                return release
                        else:
                            return upload
                    else:
                        return cp
                else:
                    return tar
            else:
                return checkout
        else:
            if self.target:
                host = self.target
                # print self.target
                self.env = "prod"
                package_path = '/apps/packages/'
                tarfile_path = os.path.join(package_path, 'releases')
                project_dir = os.path.join(package_path, self.project)
                saltmaster_dir = '/srv/salt/prod/packages/'

                url_data = get_url(self.project)
                url = url_data['url']
                owner = url_data['owner']

                dirname = self.project + '_prod_' + self.branch + '_' + self.tag
                filename = self.project + '_prod_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d")
                tarfilename = self.project + '_prod_' + self.branch + '_' + self.tag + '_' + time.strftime("%Y%m%d") + '.tar.gz'
                record = {
                    'project_name': self.project,
                    'project_owner': owner,
                    'project_env': 'PROD',
                    'project_type': self.type,
                    'deploy_branch': self.branch,
                    'deploy_tag': self.tag
                }
                cmds = self.reset_configfile(filename, '/home/wwwroot/releases/', self.config, self.env)
                checkout = self.clone_checkout(record, url, package_path, project_dir)
                if checkout['retcode'] == 0:
                    tar = self.tar_package(record, project_dir, tarfile_path, filename, self.env)
                    if tar['retcode'] == 0:
                        cp = self.cp_saltdir(record, tarfile_path, tarfilename, saltmaster_dir)
                        if cp['retcode'] == 0:
                            upload = self.saltApi_copy_dst(record, host, saltmaster_dir, tarfilename, filename, self.env)
                            if upload['retcode'] == 0:
                                release = self.saltApi_release_dir(record, host, saltmaster_dir, tarfilename, tarfile_path, package_path, dirname, filename)
                                if release['retcode'] == 0:
                                    config = self.saltApi_config_dir(cmds, host, record)
                                    return config
                                else:
                                    return release
                            else:
                                return upload
                        else:
                            return cp
                    else:
                        return tar
                else:
                    return checkout
