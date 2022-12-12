# generation_client.DefaultApi

All URIs are relative to *https://digital.iservices.rte-france.com/open_api/actual_generation/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**001**](DefaultApi.md#001) | **GET** /actual_generations_per_production_type | 
[**002**](DefaultApi.md#002) | **GET** /actual_generations_per_unit | 
[**003**](DefaultApi.md#003) | **GET** /water_reserves | 
[**004**](DefaultApi.md#004) | **GET** /generation_mix_15min_time_scale | 


# **001**
> ActualGenerationsPerProductionTypeObj 001(start_date=start_date, end_date=end_date)



This resource is for retrieving data about actual generation aggregated by sector on an intradaily basis for net generation injected into the network.

### Example
```python
from __future__ import print_function
import time
import generation_client
from generation_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = generation_client.DefaultApi()
start_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
end_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)

try:
    api_response = api_instance.001(start_date=start_date, end_date=end_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->001: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**| Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **end_date** | **datetime**| Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 

### Return type

[**ActualGenerationsPerProductionTypeObj**](ActualGenerationsPerProductionTypeObj.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **002**
> ActualGenerationsPerUnitObj 002(start_date=start_date, end_date=end_date, unit_eic_code=unit_eic_code)



This resource is for retrieving data about actual generation aggregated by unit on an intradaily basis. Data about actual generation is put together for the upcoming hour using measurements taken remotely on RTE's network. It relates to net generation injected into the network. For units that are not generating, this figure can be negative as a result of the site’s consumption.

### Example
```python
from __future__ import print_function
import time
import generation_client
from generation_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = generation_client.DefaultApi()
start_date = '2013-10-20T19:20:30+01:00' # datetime | Search start date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
end_date = '2013-10-20T19:20:30+01:00' # datetime | Search end date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
unit_eic_code = 'unit_eic_code_example' # str | Unit's EIC code (optional)

try:
    api_response = api_instance.002(start_date=start_date, end_date=end_date, unit_eic_code=unit_eic_code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->002: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**| Search start date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **end_date** | **datetime**| Search end date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **unit_eic_code** | **str**| Unit&#39;s EIC code | [optional] 

### Return type

[**ActualGenerationsPerUnitObj**](ActualGenerationsPerUnitObj.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **003**
> WaterReservesObj 003(start_date=start_date, end_date=end_date)



This resource is for retrieving data about hydraulic stocks. Hydraulic stocks for France are the aggregated weekly fill rates of reservoirs and lake-type hydraulic storage plants as recorded on Monday at 0.00 AM. They are expressed in MWh and sent by the generators to RTE, which then aggregates the data before publishing it. This data is published on Wednesdays at 12:30 PM, or the day after if Wednesday is a bank holiday.

### Example
```python
from __future__ import print_function
import time
import generation_client
from generation_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = generation_client.DefaultApi()
start_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
end_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)

try:
    api_response = api_instance.003(start_date=start_date, end_date=end_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->003: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**| Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **end_date** | **datetime**| Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 

### Return type

[**WaterReservesObj**](WaterReservesObj.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **004**
> GenerationMix15minTimeScaleObj 004(start_date=start_date, end_date=end_date, production_type=production_type, production_subtype=production_subtype)



This resource is for retrieving data about actual power generated from the overall power mix, which corresponds to net generation injected into the network. Unlike the 'actual_generations_per_production_type' resource, which returned an average for data taken over an hour, the values that this resource retrieves are discrete values every 15 minutes.

### Example
```python
from __future__ import print_function
import time
import generation_client
from generation_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = generation_client.DefaultApi()
start_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
end_date = '2013-10-20T19:20:30+01:00' # datetime | Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) (optional)
production_type = ['production_type_example'] # list[str] | Generating sector (optional)
production_subtype = ['production_subtype_example'] # list[str] | Generating sub-sector (optional)

try:
    api_response = api_instance.004(start_date=start_date, end_date=end_date, production_type=production_type, production_subtype=production_subtype)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->004: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**| Forecast search start date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **end_date** | **datetime**| Forecast search end date (YYYY-MM-DDThh:mm:sszzzzzz) | [optional] 
 **production_type** | [**list[str]**](str.md)| Generating sector | [optional] 
 **production_subtype** | [**list[str]**](str.md)| Generating sub-sector | [optional] 

### Return type

[**GenerationMix15minTimeScaleObj**](GenerationMix15minTimeScaleObj.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

