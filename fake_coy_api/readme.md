# Fake-COY-API

## Overview

This FastAPI application provides endpoints to fetch paginated lists of companies and their employees. The data is generated using a fake data generator and stored in memory. You can filter the data by various criteria and retrieve it in a paginated format. API key authentication is required to access the endpoints.

### API Endpoints

1. **Get Companies**: `/companies`
2. **Get Employees by Company ID**: `/companies/{company_id}/employees`
3. **Update Company Valuation**: `/companies/update-valuation`

### Authentication

All endpoints require an API key for authentication. The API key must be passed in the `x-api-key` header.

### API Key Example

```bash
x-api-key: mysecretkey
```

### Base URL

The API is hosted at `http://localhost:8000/`.

## Endpoints

### 1. Get Companies

- **Endpoint:** `/companies`
- **Method:** `GET`
- **Authentication:** API key required (`x-api-key`)
- **Description:** Returns a paginated list of companies with optional filtering by industry and date fields.

#### Query Parameters:

- `page` (int): Page number (default: 1)
- `size` (int): Number of items per page (default: 10, max: 100)
- `industry` (str, optional): Filter by industry
- `start_dt` (datetime, optional): Filter companies updated after this date
- `end_dt` (datetime, optional): Filter companies updated before this date (requires `start_dt` to be provided)

#### Response:

Returns a JSON object containing the paginated list of companies without employee data.

```json
{
    "items": [
        {
            "id": 1,
            "name": "Company A",
            "industry": "Tech",
            "created_at": "2023-08-20T00:00:00",
            "updated_at": "2023-08-21T00:00:00",
            "valuation": 100000000
        }
    ],
    "total": 100,
    "page": 1,
    "size": 10,
    "total_pages": 10
}
```

#### Example Request with Python `requests`:

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "mysecretkey"

response = requests.get(
    f"{BASE_URL}/companies",
    headers={"x-api-key": API_KEY},
    params={"page": 1, "size": 10, "industry": "Health"}
)

if response.status_code == 200:
    print(response.json())
else:
    print("Failed:", response.status_code, response.text)
```

### 2. Get Employees by Company ID

- **Endpoint:** `/companies/{company_id}/employees`
- **Method:** `GET`
- **Authentication:** API key required (`x-api-key`)
- **Description:** Returns a paginated list of employees for a specific company, with optional filtering by job title and date fields.

#### Path Parameters:

- `company_id` (int): The ID of the company

#### Query Parameters:

- `page` (int): Page number (default: 1)
- `size` (int): Number of items per page (default: 10, max: 100)
- `job_title` (str, optional): Filter by job title
- `start_dt` (datetime, optional): Filter employees updated after this date
- `end_dt` (datetime, optional): Filter employees updated before this date (requires `start_dt` to be provided)

#### Response:

Returns a JSON object containing the paginated list of employees.

```json
{
    "items": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "job_title": "Engineer",
            "email": "john.doe@example.com",
            "created_at": "2023-08-20T00:00:00",
            "updated_at": "2023-08-21T00:00:00"
        }
    ],
    "total": 50,
    "page": 1,
    "size": 10,
    "total_pages": 5
}
```

#### Example Request with Python `requests`:

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "mysecretkey"

company_id = 1

response = requests.get(
    f"{BASE_URL}/companies/{company_id}/employees",
    headers={"x-api-key": API_KEY},
    params={"page": 1, "size": 10, "job_title": "Engineer"}
)

if response.status_code == 200:
    print(response.json())
else:
    print("Failed:", response.status_code, response.text)
```

### 3. Update Company Valuation

- **Endpoint:** `/companies/update-valuation`
- **Method:** `GET`
- **Authentication:** API key required (`x-api-key`)
- **Description:** Randomly selects up to 10 companies and updates their valuations.

#### Response:

Returns a JSON list of companies with updated valuations.

```json
[
    {
        "id": 1,
        "name": "Company A"
    },
    {
        "id": 5,
        "name": "Company B"
    }
]
```

#### Example Request with Python `requests`:

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "mysecretkey"

response = requests.get(
    f"{BASE_URL}/companies/update-valuation",
    headers={"x-api-key": API_KEY}
)

if response.status_code == 200:
    print(response.json())
else:
    print("Failed:", response.status_code, response.text)
```

## Using `dlt`'s `RESTClient`

You can also use `dlt`'s `RESTClient` to interact with the API. Below are examples for both endpoints.

### 1. Fetch Companies with `dlt.RESTClient`

```python
from requests import Request, Response
from dlt.sources.helpers.rest_client.paginators import RangePaginator
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
from dlt.sources.helpers.rest_client import RESTClient


client = RESTClient(
    base_url="http://localhost:8000/",
    paginator=RangePaginator(param_name='page', initial_value=1, value_step=1, total_path='total'),
    auth = APIKeyAuth(api_key="mysecretkey", location="header", name="x-api-key"),
    data_selector = "$.items" # not compulsory, client can detect the data selector
)

# Fetch companies with pagination
for company_batch in client.paginate("/companies", params={"size": 10, "industry": "Health"}):
    for company in company_batch:
        print(company)
    break # to prevent printing out too many records
```

### 2. Fetch Employees by Company ID with `dlt.RESTClient`

```python
company_id = 1

for employee_batch in client.paginate(f"/companies/{company_id}/employees"):
    for employee in employee_batch:
        print(employee)
    break
```

## Conclusion

This API allows you to fetch paginated lists of companies and their employees with optional filtering by various criteria. The API requires an API key for authentication. You can interact with the API using Python's `requests` library or `dlt`'s `RESTClient` for more advanced use cases.

For more details, you can access the Swagger documentation at the root URL: `http://localhost:8000/`.
