# openapi-client

NCATS Translator Modules Identifier Resolution Server

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.0.1
- Package version: 1.0.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage

### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import openapi_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ncats.translator.identifiers.client.openapi_client.openapi_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
import pprint

from ncats.translator.identifiers.client.openapi_client import Configuration, ApiClient, AdminsApi, IdentifierMap
from ncats.translator.identifiers.client.openapi_client.rest import ApiException
from pprint import pprint

configuration = Configuration()

# Defining host is optional and default to http://identifiers
configuration.host = "http://identifiers"

# Create an instance of the API class
api_instance = AdminsApi(ApiClient(configuration))
identifier_map = IdentifierMap() # IdentifierMap | Identifier map to be uploaded (optional)

try:
    # Identifier Resolver map initial creation
    api_response = api_instance.load_identifier_map(identifier_map=identifier_map)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminsApi->load_identifier_map: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://identifiers*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AdminsApi* | [**load_identifier_map**](docs/AdminsApi.md#load_identifier_map) | **POST** /identifier_map | Identifier Resolver map initial creation
*AdminsApi* | [**update_identifier_map**](docs/AdminsApi.md#update_identifier_map) | **PUT** /identifier_map | Identifier Resolver map update
*PublicApi* | [**identifier_list**](docs/PublicApi.md#identifier_list) | **POST** /identifier_list | post a list of identifiers
*PublicApi* | [**list_identifier_keys**](docs/PublicApi.md#list_identifier_keys) | **GET** /list_identifier_keys | list of valid key strings for identifier sources and targets
*PublicApi* | [**translate**](docs/PublicApi.md#translate) | **GET** /translate | Translates list of identifiers from source to target namespace 
*PublicApi* | [**translate_one**](docs/PublicApi.md#translate_one) | **GET** /translate_one | translates one identifier source to target namespace


## Documentation For Models

 - [IdentifierListId](docs/IdentifierListId.md)
 - [IdentifierMap](docs/IdentifierMap.md)
 - [IdentifierMapId](docs/IdentifierMapId.md)
 - [IdentifierMapping](docs/IdentifierMapping.md)
 - [QueryId](docs/QueryId.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Author

richard@starinformatics.com

