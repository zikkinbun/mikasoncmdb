import os
from base import *

DEBUG = (os.environ['DEBUG'].lower() == 'true')
# DEBUG = False

# ALLOWED_HOSTS = [host.strip() for host in os.environ['ALLOWED_HOSTS'].split(',')]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deploySystem',
        'USER': 'db_admin',
        'PASSWORD': 'db_admin2015',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP
        'PORT': ''   # Set to empty string for default.
    }
}
