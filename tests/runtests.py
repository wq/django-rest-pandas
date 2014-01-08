import sys
from django.conf import settings


def main():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'pandas_test.db',
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=(
            'tests.testapp',
        ),
    )

    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    result = test_runner.run_tests((
        'tests.testapp',
    ))
    sys.exit(result)

if __name__ == "__main__":
    main()
