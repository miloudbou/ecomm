from pathlib import Path
import os
import mimetypes

# إعدادات PayPal
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")  # الوضع الافتراضي هو sandbox

mimetypes.add_type("text/css", ".css", True)



# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent



# مفتاح الأمان (يجب تغييره في بيئة الإنتاج)
SECRET_KEY = 'django-insecure-*&w$kaq9v8dfmmhr(u!g)%ep6r3-fnds&p7mlg(w)kfduvc-mq'

# وضع التصحيح (يجب أن يكون False في بيئة الإنتاج)
DEBUG = True

# السماح بالوصول إلى المشروع من هذه النطاقات
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',  # التطبيق الخاص بالمنتجات
    'rest_framework',
    'django_celery_beat',
    
   ]

# الوسائط الوسطية (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    

]

# إعدادات عنوان URL الجذر
ROOT_URLCONF = 'ecommerce_project.urls'

# إعدادات القوالب (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # مسار مجلد القوالب
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# تطبيق WSGI
WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# قاعدة البيانات (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "database/ecommerce.db",  # تغيير المسار إلى القاعدة الصحيحة
    }
}


# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# إعدادات اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# إعدادات الملفات الثابتة (Static Files)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"  # مسار الملفات الثابتة عند استخدام collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # المسار إلى مجلد static
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# نوع المفتاح الافتراضي للحقول الأساسية
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# إعداد Celery لاستخدام Redis كوسيط للرسائل
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# إعدادات PayPal
PAYPAL_CLIENT_ID = 'AfQ-M7Ou6bPLtpaDD1_y7UaZseC_8H6XvTu5fL2z9LfAksz0QJgbRo76g1r-pPPRptjpmeVYL-EfcXqY'
PAYPAL_CLIENT_SECRET = 'ECFRs8l7DXe-Zzuk_nnGvm2FwXDh2hNA6v45ks4-jR-OoXFHmaA2mm7FtZ-BzfQPssZfuD-YjeNQX2tN'
PAYPAL_MODE = "live"  # استخدم 'live'

# إعدادات العملة
DEFAULT_CURRENCY = "USD"  # العملة الافتراضية
SUPPORTED_CURRENCIES = ["USD", "DZD"]  # العملات المدعومة

# سعر الصرف الحالي للدينار الجزائري مقابل الدولار (يجب تحديثه دوريًا)
EXCHANGE_RATE_DZD_TO_USD = 0.0073  # 1 DZD = 0.0073 USD

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # استخدم SMTP الخاص بمزود الخدمة
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-email-password"
DEFAULT_FROM_EMAIL = "no-reply@yourstore.com"
DEFAULT_CURRENCY = "DZD"
CURRENCY_SYMBOL = "دج"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

