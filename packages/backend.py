from setuptools.build_meta import *
import warnings

import builder


default_build_wheel = build_wheel


class UnsupportedOperation(Exception):
    pass


def build_wheel(*args, **kwargs):
    if not builder.build():
        raise UnsupportedOperation(
            "Run python -m packages.builder and commit before releasing."
        )

    return default_build_wheel(*args, **kwargs)