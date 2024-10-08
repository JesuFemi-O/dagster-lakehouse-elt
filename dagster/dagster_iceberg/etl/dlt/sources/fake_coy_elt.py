import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_source,
)

from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from dlt.sources.helpers.rest_client.auth import APIKeyAuth

paginator=PageNumberPaginator(page_param='page', page=1, total_path='total')
auth = APIKeyAuth(api_key="mysecretkey", location="header", name="x-api-key")


fake_coy_config: RESTAPIConfig = {
    "client": {
        "base_url": "http://localhost:8000/",
        "auth": auth,
        "paginator": paginator
    },
    "resources": [
        {
            "name": "companies",
            "table_name": "company",
            "write_disposition": "merge",
            "primary_key": "id",
            "endpoint":{
                "path": "companies",
                 "params": {
                     "start_dt": {
                        "type": "incremental",
                        "cursor_path": "updated_at",
                     }
                    
                 }
            },
            "parallelized": True
        },
    ]
}

pipeline = dlt.pipeline(
    pipeline_name="fake_company_etl",
    destination='dremio',
    staging='filesystem',
    dataset_name="fake_companies",
    progress="log"
)

fake_coy_source = rest_api_source(fake_coy_config)