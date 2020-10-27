#!/usr/bin/python
# -*- coding: utf-8 -*-
# from datetime import datetime
from io import open
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(HERE, "VERSION")

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()
# with open("HISTORY.md", mode="r", encoding="utf-8") as f:
# history = f.read()

requirements = ["requests"]
test_requires = ["codecov", "pytest-cov", "pytest-mock", "pytest"]


if sys.argv[-1] == "publish_dev":
    os.system("python setup.py sdist bdist_wheel")
    os.system("devpi upload")
    sys.exit()
elif sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count

            self.pytest_args = ["-n", str(cpu_count()), "--boxed", "--cov=./"]
        except (ImportError, NotImplementedError):
            self.pytest_args = ["-n", "1", "--boxed", "--cov=./"]
        else:
            self.pytest_args = ["--cov=./"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


about = {}
with open(os.path.join(HERE, "blaser", "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

packages = find_packages(exclude=["tests"])

setup(
    author=about["__author__"],
    author_email=about["__author_email__"],
    classifiers=[],
    cmdclass={"test": PyTest},
    description=about["__description__"],
    download_url="{about['__github_url__']}/archive/{about['__version__']}.zip",
    extras_require={"docs": ["Sphinx", "SimpleHTTPServer", "sphinx_rtd_theme"]},
    entry_points={},
    include_package_data=True,
    install_requires=requirements,
    license=[""],
    long_description=readme,
    name=about["__title__"],
    package_data={"": ["LICENSE", "NOTICE"], "blaser": [""]},
    package_dir={"blaser": "blaser"},
    packages=packages,
    project_urls=about["__urls__"],
    python_requires=">=3.6",
    tests_require=test_requires,
    url=about["__url__"],
    version=about["__version__"],
    zip_safe=False,
)
