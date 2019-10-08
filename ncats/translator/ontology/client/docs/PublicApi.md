# openapi_client.PublicApi

All URIs are relative to *http://0.0.0.0:8082*

Method | HTTP request | Description
------------- | ------------- | -------------
[**compute_jaccard**](PublicApi.md#compute_jaccard) | **POST** /compute_jaccard | post a list of input genes and initiate a Jaccard similarity computation
[**get_results**](PublicApi.md#get_results) | **GET** /results | Retrieves a list of similarity results when ready 


# **compute_jaccard**
> ComputationIdentifier compute_jaccard(computation_input=computation_input)

post a list of input genes and initiate a Jaccard similarity computation

Post a list of input genes and initiate a Jaccard similarity computation 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()
computation_input = openapi_client.ComputationInput() # ComputationInput | List of input genes upon which to compute Jaccard similarity  (optional)

try:
    # post a list of input genes and initiate a Jaccard similarity computation
    api_response = api_instance.compute_jaccard(computation_input=computation_input)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->compute_jaccard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **computation_input** | [**ComputationInput**](ComputationInput.md)| List of input genes upon which to compute Jaccard similarity  | [optional] 

### Return type

[**ComputationIdentifier**](ComputationIdentifier.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Jaccard similarity computation initiated on the server  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_results**
> Results get_results(computation_id)

Retrieves a list of similarity results when ready 

Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes 

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.PublicApi()
computation_id = 'computation_id_example' # str | Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes 

try:
    # Retrieves a list of similarity results when ready 
    api_response = api_instance.get_results(computation_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicApi->get_results: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **computation_id** | **str**| Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes  | 

### Return type

[**Results**](Results.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | computation successful, results returned |  -  |
**102** | The requested computation is still in process without error, but no results are yet available.  |  -  |
**400** | bad input target parameter |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

