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
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    else:
        # Pandoc's RST tables don't work with rst2html...
        subprocess.call(
            ['patch', 'README.rst', 'README.rst.patch']
        )

    # Attempt to load output
    try:
        readme = open('README.rst')
    except IOError:
        return LONG_DESCRIPTION
    else:
        return readme.read()

setup(
    name='rest-pandas',
    version='0.2.0',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    test_suite='tests',
    tests_require=['wq.io>=0.6.0'],
)
