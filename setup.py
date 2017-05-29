# :coding: utf-8

import os
import re

from setuptools import setup, find_packages


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = os.path.join(ROOT_PATH, "resource")
SOURCE_PATH = os.path.join(ROOT_PATH, "source")
README_PATH = os.path.join(ROOT_PATH, "README.rst")

PACKAGE_NAME = "champollion"

# Read version from source.
with open(
    os.path.join(SOURCE_PATH, PACKAGE_NAME, "_version.py")
) as _version_file:
    VERSION = re.match(
        r".*__version__ = \"(.*?)\"", _version_file.read(), re.DOTALL
    ).group(1)


# Compute dependencies.
INSTALL_REQUIRES = [
    "sphinx >= 1.2.2, < 2"
]
DOC_REQUIRES = [
    "sphinx_rtd_theme >= 0.1.6, < 1",
    "lowdown >= 0.1.0, < 2",
]
TEST_REQUIRES = [
    "pytest-runner >= 2.7, < 3",
    "pytest >= 2.9, < 3",
    "pytest-mock >= 0.11, < 1",
    "pytest-catchlog >= 1, < 2",
    "pytest-xdist >= 1.1, < 2",
    "pytest-cov >= 2, < 3"
]

setup(
    name="champollion",
    version=VERSION,
    description="Generate documentation from ES6 source files.",
    long_description=open(README_PATH).read(),
    url="http://github.com/buddly27/champollion",
    keywords="",
    author="Jeremy Retailleau",
    packages=find_packages(SOURCE_PATH),
    package_dir={
        "": "source"
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require={
        "doc": DOC_REQUIRES,
        "sub_module": TEST_REQUIRES,
        "dev": DOC_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False,
    platforms="any",
)
