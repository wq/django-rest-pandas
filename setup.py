import os
import sys
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Serves up Pandas dataframes via the Django REST Framework for client-side (i.e. d3.js) visualizations
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()

setup(
    name='rest-pandas',
    version='0.1.0-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/django-rest-pandas',
    license='MIT',
    packages=['rest_pandas'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=[
        'djangorestframework>=2.3.10',
        'pandas'
    ],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis'
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    test_suite='tests.runtests.main',
    tests_require=['wq.io'],
)
