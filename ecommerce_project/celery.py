import os
from celery import Celery
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

# تعيين الإعدادات الافتراضية لـ Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")

# إنشاء كائن Celery
app = Celery("ecommerce_project")

# تحميل إعدادات Celery من ملف settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# اكتشاف المهام تلقائيًا من التطبيقات المسجلة في المشروع
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
