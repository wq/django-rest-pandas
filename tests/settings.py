SECRET_KEY = '1234'
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'tests.testapp',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = "tests.urls"
