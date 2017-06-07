import os
from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deploySystem',
        'USER': 'db_admin',
        'PASSWORD': 'db_admin2016',
        'HOST': '112.74.188.202',
        'PORT': '3306'
    }
}

BROKER_URL='redis://:gdrdev2016@112.74.182.80:6379/7'
CELERY_RESULT_BACKEND='redis://:gdrdev2016@112.74.182.80:6379/8'
