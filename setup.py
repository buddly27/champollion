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
    "sphinx >= 1.7.5, < 1.8"
]
DOC_REQUIRES = [
    "sphinx_rtd_theme >= 0.2.0, < 1",
    "lowdown >= 0.1.0, < 2",
]
TEST_REQUIRES = [
    "pytest-runner >= 2.11, < 3",
    "pytest >= 3.1.2, < 4",
    "pytest-mock >= 0.6, < 1",
    "pytest-xdist >= 1.1, < 2",
    "pytest-cov >= 2, < 3"
]


# Readthedocs requires Sphinx extensions to be specified as part of
# install_requires in order to build properly.
if os.environ.get("READTHEDOCS", None) == "True":
    INSTALL_REQUIRES.extend(DOC_REQUIRES)


setup(
    name="champollion",
    version=VERSION,
    description="Sphinx extension to document javascript code.",
    long_description=open(README_PATH).read(),
    url="http://github.com/buddly27/champollion",
    keywords=["sphinx", "javascript", "es6", "restructuredtext", "auto"],
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
        "test": TEST_REQUIRES,
        "dev": DOC_REQUIRES + TEST_REQUIRES
    },
    zip_safe=False,
    platforms="any",
)
