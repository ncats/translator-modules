# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "ncats_translator_modules_identifiers_openapi_server"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion==2.0.0",
    "swagger-ui-bundle==0.0.2",
    "python_dateutil==2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="NCATS Translator Modules Identifier Resolution Server",
    author_email="richard@starinformatics.com",
    url="",
    keywords=["OpenAPI", "NCATS Translator Modules Identifier Resolution Server"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']
    },
    long_description="""\
    NCATS Translator Modules Identifier Resolution Server
    """
)

