SECRET_KEY = "1234"
INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "tests.testapp",
    "rest_pandas",
    "rest_framework",
)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "rest_pandas_test.sqlite3",
    }
}
ROOT_URLCONF = "tests.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

TIME_ZONE = "UTC"
DEBUG = True


try:
    import matplotlib  # noqa
except ImportError:
    HAS_MATPLOTLIB = False
else:
    HAS_MATPLOTLIB = True


try:
    import django_pandas  # noqa
except ImportError:
    HAS_DJANGO_PANDAS = False
else:
    HAS_DJANGO_PANDAS = True


from django import VERSION  # noqa

HAS_DJANGO_4 = VERSION[0] == 4
