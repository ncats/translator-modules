# openapi_client.PublicApi

All URIs are relative to *http://0.0.0.0:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**identifier_list**](PublicApi.md#identifier_list) | **POST** /identifier_list | post a list of identifiers
[**list_identifier_keys**](PublicApi.md#list_identifier_keys) | **GET** /list_identifier_keys | list of valid key strings for identifier sources and targets
[**translate**](PublicApi.md#translate) | **GET** /translate | Translates list of identifiers from source to target namespace 
[**translate_one**](PublicApi.md#translate_one) | **GET** /translate_one | translates one identifier source to target namespace


# **identifier_list**
> IdentifierListId identifier_list(request_body=request_body)

post a list of identifiers

Post a list of source identifiers for subsequent translation 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()
request_body = ['request_body_example'] # list[str] | Identifier list to post on server (for translation)  (optional)

try:
    # post a list of identifiers
    api_response = api_instance.identifier_list(request_body=request_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->identifier_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**list[str]**](str.md)| Identifier list to post on server (for translation)  | [optional] 

### Return type

[**IdentifierListId**](IdentifierListId.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Identification of identifier list created on server  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_identifier_keys**
> list[str] list_identifier_keys()

list of valid key strings for identifier sources and targets

Returns list of valid key strings for source and target parameters in other API calls 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()

try:
    # list of valid key strings for identifier sources and targets
    api_response = api_instance.list_identifier_keys()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->list_identifier_keys: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | list of valid key strings for identifier sources and targets  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **translate**
> list[IdentifierMapping] translate(list_identifier, target_namespace)

Translates list of identifiers from source to target namespace 

Translates a previously posted list of identifiers from source namespace to a specified target namespace 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()
list_identifier = 'list_identifier_example' # str | UUID from identifier_list post of source identifiers 
target_namespace = 'target_namespace_example' # str | Target namespace for mapping of source identifiers 

try:
    # Translates list of identifiers from source to target namespace 
    api_response = api_instance.translate(list_identifier, target_namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->translate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_identifier** | **str**| UUID from identifier_list post of source identifiers  | 
 **target_namespace** | **str**| Target namespace for mapping of source identifiers  | 

### Return type

[**list[IdentifierMapping]**](IdentifierMapping.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | translation successful |  -  |
**400** | bad input target parameter |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **translate_one**
> IdentifierMapping translate_one(source_identifier, target_namespace)

translates one identifier source to target namespace

Returns mapping of identifier source to its equivalent identifier in the specified target namespace 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()
source_identifier = 'source_identifier_example' # str | single source identifier to be mapped onto the target 
target_namespace = 'target_namespace_example' # str | target namespace for the mapping of the source 

try:
    # translates one identifier source to target namespace
    api_response = api_instance.translate_one(source_identifier, target_namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->translate_one: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **source_identifier** | **str**| single source identifier to be mapped onto the target  | 
 **target_namespace** | **str**| target namespace for the mapping of the source  | 

### Return type

[**IdentifierMapping**](IdentifierMapping.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | translation successful |  -  |
**400** | bad input target parameter |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

