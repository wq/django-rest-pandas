from os.path import join, dirname, exists
import sys
import subprocess
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Serves up Pandas dataframes via the Django REST Framework for client-side (i.e. d3.js) visualizations
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Check for existing file (Pandoc's RST tables don't work with rst2html...)
    path = join(dirname(__file__), 'README.rst')
    if not exists(path):
        # Attempt to run pandoc on markdown file
        try:
            subprocess.call(
                ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
            )
        except OSError:
            return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(path)
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()

setup(
    name='rest-pandas',
    version='0.1.1',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/django-rest-pandas',
    license='MIT',
    packages=['rest_pandas'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=[
        'djangorestframework>=2.3.12',
        'pandas>=0.13.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    test_suite='tests.runtests.main',
    tests_require=['wq.io'],
)
