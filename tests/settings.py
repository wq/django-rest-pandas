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
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = "tests.urls"
TEMPLATES = [
    {
        'BACKEND': 'django_mustache.Mustache',
        'APP_DIRS': True,
    },
]
