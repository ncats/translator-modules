# ara_client.QueryApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**query**](QueryApi.md#query) | **POST** /query | Query reasoner via one of several inputs


# **query**
> Message query(request_body)

Query reasoner via one of several inputs

### Example

```python
from __future__ import print_function
import time
import ara_client
from ara_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ara_client.QueryApi()
request_body = None # dict(str, object) | Query information to be submitted

try:
    # Query reasoner via one of several inputs
    api_response = api_instance.query(request_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueryApi->query: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**dict(str, object)**](object.md)| Query information to be submitted | 

### Return type

[**Message**](Message.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | successful operation |  -  |
**400** | Invalid status value |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

