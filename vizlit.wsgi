import os, sys
sys.path.append('/var/www/site/django')
sys.path.append('/var/www/site/django/vizlit')
os.environ['DJANGO_SETTINGS_MODULE'] = 'vizlit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
