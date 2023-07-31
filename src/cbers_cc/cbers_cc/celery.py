

import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbers_cc.settings')
 
app = Celery('cbers_cc')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()