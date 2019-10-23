# openapi_client.AdminsApi

All URIs are relative to *http://0.0.0.0:8081*

Method | HTTP request | Description
------------- | ------------- | -------------
[**load_identifier_map**](AdminsApi.md#load_identifier_map) | **POST** /identifier_map | Identifier Resolver map initial creation
[**update_identifier_map**](AdminsApi.md#update_identifier_map) | **PUT** /identifier_map | Identifier Resolver map update


# **load_identifier_map**
> QueryId load_identifier_map(identifier_map=identifier_map)

Identifier Resolver map initial creation

Adds an identifier map to the Identifier Resolver 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.AdminsApi()
identifier_map = openapi_client.IdentifierMap() # IdentifierMap | Identifier map to be uploaded (optional)

try:
    # Identifier Resolver map initial creation
    api_response = api_instance.load_identifier_map(identifier_map=identifier_map)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminsApi->load_identifier_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier_map** | [**IdentifierMap**](IdentifierMap.md)| Identifier map to be uploaded | [optional] 

### Return type

[**QueryId**](QueryId.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Identification of identifier map uploaded to server  |  -  |
**400** | invalid input, object invalid |  -  |
**409** | Identifier map already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_identifier_map**
> QueryId update_identifier_map(identifier_map=identifier_map)

Identifier Resolver map update

Updates identifier map in the Identifier Resolver 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.AdminsApi()
identifier_map = openapi_client.IdentifierMap() # IdentifierMap | Identifier map to be updated (optional)

try:
    # Identifier Resolver map update
    api_response = api_instance.update_identifier_map(identifier_map=identifier_map)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminsApi->update_identifier_map: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier_map** | [**IdentifierMap**](IdentifierMap.md)| Identifier map to be updated | [optional] 

### Return type

[**QueryId**](QueryId.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Identification of identifier map updated on server  |  -  |
**400** | invalid input, object invalid |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

