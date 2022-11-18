from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import warnings
import pathlib


LONG_DESCRIPTION = (
    "Serves up pandas dataframes via the Django REST Framework for client-side"
    "(i.e. d3.js) visualizations"
)


class BuildJS(build_py):
    def run(self):
        try:
            version = (
                pathlib.Path(__file__).parent
                / "packages"
                / "analyst"
                / "src"
                / "version.js"
            )
            version.write_text(
                f'export default "{self.distribution.get_version()}";'
            )
            subprocess.check_call(["npm", "install"])
            subprocess.check_call(["npm", "run", "build"])
        except BaseException as e:
            warnings.warn("Skipping JS build: {}".format(e))
        super().run()


def readme():
    try:
        readme = open("README.md")
    except IOError:
        return LONG_DESCRIPTION
    else:
        return readme.read()


setup(
    name="rest-pandas",
    use_scm_version=True,
    author="S. Andrew Sheppard",
    author_email="andrew@wq.io",
    url="https://github.com/wq/django-rest-pandas",
    license="MIT",
    packages=["rest_pandas"],
    package_data={
        "rest_pandas": [
            "templates/rest_pandas/*.html",
            "static/rest_pandas/js/*.*",
            "static/app/js/*.*",
        ]
    },
    description=LONG_DESCRIPTION.strip(),
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=[
        "djangorestframework>=3.3.1",
        "pandas>=0.19.0",
    ],
    classifiers=[
        "Framework :: Django",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    test_suite="tests",
    setup_requires=[
        "setuptools_scm",
    ],
    cmdclass={"build_py": BuildJS},
    project_urls={
        "Homepage": "https://django-rest-pandas.wq.io/",
        "Documentation": "https://django-rest-pandas.wq.io/",
        "Source": "https://github.com/wq/django-rest-pandas",
        "Release Notes": "https://django-rest-pandas.wq.io/releases/",
        "Issues": "https://github.com/wq/django-rest-pandas/issues",
    },
)
