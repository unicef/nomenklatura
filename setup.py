#!/usr/bin/env python
import ast
import os.path
import re
from codecs import open

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.dirname(__file__))
init = os.path.join(ROOT, 'nomenklatura', '__init__.py')
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))

dependency_links = set()
setup(
    name=NAME,
    version=VERSION,
    description="Make record linkages on the web.",
    long_description='',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Flask',
        'Framework :: Flake8',
    ],
    keywords='data mapping identity linkage record',
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='http://okfn.org',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
    ],
    tests_require=[],
    entry_points=""" """,
)
