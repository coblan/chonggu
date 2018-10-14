from .base import *
from .logging import*

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'chonggu',
        #'USER': 'postgres',
        #'PASSWORD': '123',
        'USER': 'root',
        'PASSWORD': 'root533',        
        'HOST': '127.0.0.1', 
        'PORT': '5432', 
    },
}


XUNCHA_HOST = 'http://10.231.18.23:8199'

SANGO_BRIDGE='http://10.231.18.23:8499'

ALLOWED_HOSTS=['10.231.18.23']


