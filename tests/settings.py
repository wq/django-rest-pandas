SECRET_KEY = '1234'
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'tests.testapp',
    'rest_pandas',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'rest_pandas_test.sqlite3',
    }
}
ROOT_URLCONF = "tests.urls"
TEMPLATES = [
    {
        'BACKEND': 'django_mustache.Mustache',
        'APP_DIRS': True,
    },
]

DEBUG = True


try:
    import matplotlib   # noqa
except ImportError:
    HAS_MATPLOTLIB = False
else:
    HAS_MATPLOTLIB = True


try:
   import django_pandas   # noqa
except ImportError:
    HAS_DJANGO_PANDAS = False
else:
    HAS_DJANGO_PANDAS = True
