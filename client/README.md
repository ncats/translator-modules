# OpenAPI Generated ARA Client

This server folder contains the implementation of an ARA web service client for the NCATS workflows implementing the 
[NCATS Reasoner Application Programming Interface](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI).

This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 0.9.2
- Package version: 0.9.2

- Build package: org.openapitools.codegen.languages.PythonClientCodegen

For more information, please visit [http://starinformatics.com](http://starinformatics.com)

## Requirements.

Python 3.7

## Installation & Usage

### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/ncats/translator-modules.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ncats/translator-modules.git`)

Then import the package:
```python
import ara_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import ara_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function

from ara_client.api_client import ApiClient
from ara_client.api.predicates_api import PredicatesApi
from ara_client.rest import ApiException
from ara_client.configuration import Configuration
from pprint import pprint

# Defining host is optional and default to http://localhost
configuration = Configuration()

# Create an instance of the API class
api_instance = PredicatesApi(ApiClient(configuration))

try:
    # Get supported relationships by source and target
    api_response = api_instance.predicates_get()
    pprint(api_response)

except ApiException as e:
    print("Exception when calling PredicatesApi->predicates_get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*PredicatesApi* | [**predicates_get**](docs/PredicatesApi.md#predicates_get) | **GET** /predicates | Get supported relationships by source and target
*QueryApi* | [**query**](docs/QueryApi.md#query) | **POST** /query | Query reasoner via one of several inputs


## Documentation For Models

 - [Credentials](docs/Credentials.md)
 - [Edge](docs/Edge.md)
 - [EdgeBinding](docs/EdgeBinding.md)
 - [KnowledgeGraph](docs/KnowledgeGraph.md)
 - [Message](docs/Message.md)
 - [Node](docs/Node.md)
 - [NodeBinding](docs/NodeBinding.md)
 - [QEdge](docs/QEdge.md)
 - [QNode](docs/QNode.md)
 - [Query](docs/Query.md)
 - [QueryGraph](docs/QueryGraph.md)
 - [RemoteKnowledgeGraph](docs/RemoteKnowledgeGraph.md)
 - [Result](docs/Result.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Authors

Reasoner API:     edeutsch@systemsbiology.org
Workflow ARA API: richard@starinformatics.com