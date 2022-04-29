from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','timetravel.settings')   #Here change the project name accordingly..

app = Celery('timetravel')  #Please change the project name accordingly..

app.conf.enable_utc  = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings',namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
	print(f'Request : {self.request!r}') 
