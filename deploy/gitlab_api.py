#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required

import requests
import json

@csrf_exempt
def get_project(request):  # search the project from gitlab
    # project_url = 'http://112.74.182.80:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    project_url = 'http://39.108.141.79:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    r = requests.get(project_url)
    datas = r.json()
    # print datas
    # project_list = []
    # project_name = []
    projects = []
    for data in datas:
        # project_list.append(data[u'id'])
        # project_name.append(data[u'name'])
        # braches = get_branches_api(data[u'id'])
        # tags = get_tag_api(data[u'id'])
        project = {
            'id': data[u'id'],
            'name': data[u'name'],
            # 'branches': braches,
            # 'tags': tags
            }
        projects.append(project)
    # projects = [dict(zip(project_list, project_name))]
    r =  json.dumps(projects)
    # print r
    return HttpResponse(r)

@csrf_exempt
def get_tag(request):  # get all tags of the project
    if request.POST:
        # project_id = request.POST.get('project_id', '')
        project_id = json.loads(request.body)[u'project_id']
        # print json.loads(request.body)[u'project_id']
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
            tag = {
                'name': data[u'name'],
                'message': data[u'message'],
                }
            tag_list.append(tag)
        mytags = json.dumps(tag_list)
        return HttpResponse(mytags)

@csrf_exempt
def get_branches(request):
    if request.POST:
        # project_id = request.POST.get('project_id', '')
        project_id = json.loads(request.body)[u'project_id']
        # print request.body
        # print type(project_id)
        # branch_url = 'http://112.74.182.80:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
        branch_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
        print branch_url
        r = requests.get(branch_url)
        datas = r.json()
        branches_list = []
        # print datas
        for data in datas:
            branch = {
                'protected': data[u'protected'],
                'name': data[u'name'],
            }
            branches_list.append(branch)
        mybranches = json.dumps(branches_list)
        return HttpResponse(mybranches)

def get_project_api():  # search the project from gitlab
    # project_url = 'http://112.74.182.80:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    project_url = 'http://39.108.141.79:10080/api/v3/projects?per_page=50&private_token=1__kd35zHaxPyx21BnX6'
    r = requests.get(project_url)
    datas = r.json()
    projects = []
    for data in datas:
        project = {
            'id': data[u'id'],
            'name': data[u'name'],
            }
        projects.append(project)
    # projects = [dict(zip(project_list, project_name))]
    r =  json.dumps(projects)
    # print r
    return projects

def get_tag_api(project_id):  # get all tags of the project
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
        tag_list.append(data[u'name'])
    mytags = json.dumps(tag_list)
    return mytags


def get_branches_api(project_id):
    # branch_url = 'http://112.74.182.80:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
    branch_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project_id) + "/repository/branches?private_token=1__kd35zHaxPyx21BnX6"
    # print branch_url
    r = requests.get(branch_url)
    datas = r.json()
    branches_list = []
    # print datas
    for data in datas:
        branches_list.append(data[u'name'])
    mybranches = json.dumps(branches_list)
    return mybranches

def get_url_api(project_name):
    projects = get_project_api()
    # print projects
    project_id = ''
    for project in projects:
        if project_name == project['name']:
            project_id = project['id']
            print project_id
    # request_url = 'http://112.74.182.80:10080/api/v3/projects/' + str(project_id) + "?private_token=1__kd35zHaxPyx21BnX6"
    request_url = 'http://39.108.141.79:10080/api/v3/projects/' + str(project_id) + "?private_token=1__kd35zHaxPyx21BnX6"
    r = requests.get(request_url)
    data = r.json()
    # print data
    project_url = data[u'ssh_url_to_repo']
    # print project_url
    return project_url
