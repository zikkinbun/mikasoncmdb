#!/usr/bin/env python
# coding: utf-8

import os
import sys

# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deploySystem.settings")

from django.core.wsgi import get_wsgi_application
# from django.core.handlers.wsgi import WSGIHandler
application = get_wsgi_application()
# application = WSGIHandler()
