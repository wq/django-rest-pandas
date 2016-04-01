import os
from django.test.utils import setup_test_environment
from django.core.management import call_command
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "tests.settings"
setup_test_environment()
if hasattr(django, 'setup'):
    # Django 1.7+
    django.setup()
    call_command('makemigrations', 'testapp', interactive=False)
    call_command('migrate', interactive=False)
else:
    # Django 1.6
    call_command('syncdb', interactive=False)
