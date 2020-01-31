# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "ncats_translator_modules_jaccard_similarity_openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion==2.0.0",
    "swagger-ui-bundle==0.0.2",
    "python_dateutil==2.6.0",
    "jsonschema>=3.0.1"
]

setup(
    name=NAME,
    version=VERSION,
    description="NCATS Translator Modules Ontology Jaccard Similarity Server",
    author_email="richard@starinformatics.com",
    url="",
    keywords=["OpenAPI", "NCATS Translator Modules Ontology Jaccard Similarity Server"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    NCATS Translator Modules Ontology Jaccard Similarity Server
    """
)

