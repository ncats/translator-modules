# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "ara_server"
VERSION = "0.9.2"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="OpenAPI for NCATS Biomedical Translator Reasoners",
    author_email="edeutsch@systemsbiology.org",
    url="https://github.com/ncats/translator_modules/tree/master/server",
    keywords=["OpenAPI", "OpenAPI for NCATS Biomedical Translator Reasoners"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['ara_server=ara_server.__main__:main']},
    long_description="""\
    OpenAPI for NCATS Biomedical Translator Reasoners
    """
)

