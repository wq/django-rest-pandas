import os
from django.test.utils import setup_test_environment
from django.core.management import call_command
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "tests.settings"
setup_test_environment()
django.setup()
call_command('makemigrations', 'testapp', interactive=False)
call_command('migrate', interactive=False)
