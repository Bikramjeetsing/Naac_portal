import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naac_portal.settings")

app = Celery("naac_portal")

# Load settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()
