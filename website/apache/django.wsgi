import os
import sys

path = '/srv/project/website'
if path not in sys.path:
    sys.path.insert(0, '/srv/project/website')

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
