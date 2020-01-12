# ara_client.PredicatesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**predicates_get**](PredicatesApi.md#predicates_get) | **GET** /predicates | Get supported relationships by source and target


# **predicates_get**
> dict(str, dict(str, list[str])) predicates_get()

Get supported relationships by source and target

### Example

```python
from __future__ import print_function
import time
import ara_client
from ara_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = ara_client.PredicatesApi()

try:
    # Get supported relationships by source and target
    api_response = api_instance.predicates_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PredicatesApi->predicates_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, dict(str, list[str]))**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Predicates by source and target |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

