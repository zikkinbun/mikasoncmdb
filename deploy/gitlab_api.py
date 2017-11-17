#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from server.models import ServerProjects
from server.serializers import ServerProjectsSerializers
from util.exception import BaseException, ParamException
from util.error import BaseError, CommonError

import requests
import json
import threading

class GetProjectsInfo(APIView):

    def get_project(self):
        try:
            return ServerProjects.objects.all()
        except:
            raise DatabaseError

    def post(self, request, format=None):
        request_project = RequestProject()
        # request_project.run()
        request_project.start() # 开启多线程

        projects = self.get_project()
        serializer = ServerProjectsSerializers(projects, many=True)
        datas = serializer.data
        rebuild = []
        for data in datas:
            project = {
                'pid': data['pid'],
                'name': data['name'],
                'type': data['type'],
                'ssh_url': data['ssh_url'],
                'http_url': data['http_url'],
                'branches': str(data['branches']).replace('"', '').replace('\'', '').replace('[', '').replace(']', '').split(', '),
                'tags': str(data['tags']).replace('"', '').replace('\'', '').replace('[', '').replace(']', '').split(', '),
                'configfile': data['configfile'],
                'owner': data['owner'],
                'createdate': data['createdate']
            }
            rebuild.append(project)

        response = {
            'retcode': 0,
            'retdata': rebuild
        }
        return Response(response)

class RequestProject(threading.Thread):

    def create_project(self, project={}):
        try:
            exists = ServerProjects.objects.filter(pid=project['id'])
            if exists:
                    exists.update(pid=project['id'], name=project['name'], owner=project['owner'], \
                        ssh_url=project['ssh_url'], http_url=project['http_url'], branches=project['branches'], \
                        tags=project['tags'])
            else:
                ServerProjects.objects.create(pid=project['id'], name=project['name'], owner=project['owner'], \
                    ssh_url=project['ssh_url'], http_url=project['http_url'], branches=project['branches'], \
                    tags=project['tags'])
        except:
            raise DatabaseError

    def run(self):
        project_url = 'http://39.108.141.79:10080/api/v3/projects?per_page=100&private_token=1__kd35zHaxPyx21BnX6'
        r = requests.get(project_url)
        datas = r.json()
        for data in datas:
            branches = get_branches(data['id'])
            tags = get_tag(data['id'])

            project = {
            'id': data['id'],
            'name': data['name'],
            'owner': data['owner']['name'],
            'ssh_url': str(data['ssh_url_to_repo']).replace('192.168.1.211', '39.108.141.79'),
            'http_url': str(data['http_url_to_repo']).replace('192.168.1.211', '39.108.141.79'),
            'branches': branches,
            'tags': tags
            }
            self.create_project(project)

class UpdateProjectInfo(APIView):

    def update_project(self, name, setting={}):
        try:
            project = ServerProjects.objects.filter(name=name)
            if project:
                project.update(type=setting['type'], configfile=setting['config'])
        except:
            raise DatabaseError

    def get_project(self, name):
        try:
            return ServerProjects.objects.get(name=name)
        except:
            raise DatabaseError

    def post(self, request, format=None):

        project_name = json.loads(request.body).get('name', None)
        if project_name is None:
            raise ParamException('name')
        project_type = json.loads(request.body).get('type', None)
        if project_type is None:
            raise ParamException('type')
        config = json.loads(request.body).get('config', None)
        if config is None:
            raise ParamException('config')

        setting = {
            'type': project_type,
            'config':config
        }
        self.update_project(project_name, setting)

        project = self.get_project(project_name)
        if project:
            serializer = ServerProjectsSerializers(project)
            response = {
                'retcode': 0,
                'retdata': serializer.data,
                'retmsg': 'success'
            }
            return Response(response)
        else:
            response = {
                'retcode': -1,
                'retmsg': 'failed'
            }
            return Response(response)

class GetProjects(APIView):

    def post(self, request, format=None):
        project_url = 'http://39.108.141.79:10080/api/v3/projects?per_page=100&private_token=1__kd35zHaxPyx21BnX6'
        r = requests.get(project_url)
        datas = r.json()
        projects = []
        for data in datas:
            project = {
                'id': data['id'],
                'name': data['name'],
                'owner': data['owner']['name'],
                'ssh_url': data['ssh_url_to_repo'],
                'http_url': data['http_url_to_repo'],
            }
            projects.append(project)
        response = {
            'retcode': 0,
            'retdata': projects
        }
        return Response(response)

class GetTags(APIView):

    def get_id(self, project):
        try:
            return ServerProjects.objects.get(name=project)
        except:
            raise DatabaseError

    def post(self, request, format=None):
        project_name = json.loads(request.body).get('project', None)
        if project_name is None:
            raise ParamException('project')
        project = self.get_id(project_name)

        tag_url = "http://39.108.141.79:10080/api/v3/projects/" + \
                str(project.pid) + \
                "/repository/tags?private_token=1__kd35zHaxPyx21BnX6"
        r = requests.get(tag_url)
        datas = r.json()
        tags = []
        for data in datas:
            tag = {
                'name': data[u'name'],
                'message': data[u'message'],
                }
            tags.append(tag)
        response = {
            'retcode': 0,
            'retdata': tags
        }
        return Response(response)

class GetBranchs(APIView):

    def get_id(self, project):
        try:
            return ServerProjects.objects.get(name=project)
        except:
            raise DatabaseError

    def post(self, request, format=None):
        project_name = json.loads(request.body).get('project', None)
        if project_name is None:
            raise ParamException('project')
        project = self.get_id(project_name)

        branch_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project.pid) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
        r = requests.get(branch_url)
        datas = r.json()
        branches = []
        for data in datas:
            branch = {
                'protected': data[u'protected'],
                'name': data[u'name'],
            }
            branches.append(branch)
        response = {
            'retcode': 0,
            'retdata': branches
        }
        return Response(response)

def get_project():  # search the project from gitlab
    # project_url = 'http://112.74.182.80:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    project_url = 'http://39.108.141.79:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    r = requests.get(project_url)
    datas = r.json()
    projects = []
    for data in datas:
        project = {
            'id': data[u'id'],
            'name': data[u'name'],
            'owner': data[u'owner']['name']
            }
        projects.append(project)
    # projects = [dict(zip(project_list, project_name))]
    r =  json.dumps(projects)
    # print r
    return projects

def get_tag(project_id):  # get all tags of the project
    # tag_url = "http://112.74.182.80:10080/api/v3/projects/" + \
    #         str(project_id) + \
    #         "/repository/tags?private_token=1__kd35zHaxPyx21BnX6"
    tag_url = "http://39.108.141.79:10080/api/v3/projects/" + \
            str(project_id) + \
            "/repository/tags?private_token=1__kd35zHaxPyx21BnX6"
    r = requests.get(tag_url)
    datas = r.json()
    tag_list = []
    # print datas
    for data in datas:
        tag_list.append(data['name'].encode("utf-8"))
    # mytags = json.dumps(tag_list)
    return tag_list


def get_branches(project_id):
    # branch_url = 'http://112.74.182.80:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
    branch_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
    # print branch_url
    r = requests.get(branch_url)
    datas = r.json()
    branches_list = []
    # print datas
    for data in datas:
        branches_list.append(data['name'].encode("utf-8"))
    # mybranches = json.dumps(branches_list)
    return branches_list


def get_url(project_name):
    projects = get_project()
    # print projects
    project_id = ''
    for project in projects:
        if project_name == project['name']:
            project_id = project['id']
            # print project_id
    # request_url = 'http://112.74.182.80:10080/api/v3/projects/' + str(project_id) + "?private_token=1__kd35zHaxPyx21BnX6"
    request_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project_id) + "?private_token=1__kd35zHaxPyx21BnX6"
    r = requests.get(request_url)
    data = r.json()
    # print data
    project_url = data[u'ssh_url_to_repo']
    project_owner = data[u'owner']['name']
    callback = {
        'url': project_url,
        'owner': project_owner
    }
    # print project_url
    return callback
