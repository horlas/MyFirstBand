from myfirstband.settings import *

DEBUG = False

TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['myfirstband.cedrix.org', '*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myfirstband',
        'USER': 'myfirstband',
        'PASSWORD': 'admin1234',
        'HOST': '10.0.3.15',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR , 'staticfiles')