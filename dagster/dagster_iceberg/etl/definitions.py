from dagster import Definitions, load_assets_from_modules
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_embedded_elt.sling import SlingResource
from dagster_iceberg.etl.dlt import assets as dlt_assets
from dagster_iceberg.etl.sling import assets as sling_assets
from dagster_iceberg.etl.sling.sources.customers import source_conn_resource, target_conn_resource

# add sling assets to the list too when you have them.
all_assets = load_assets_from_modules([dlt_assets, sling_assets])

print(f"Target connection name: {target_conn_resource.name}")

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": DagsterDltResource(),
        "sling":SlingResource(
            connections=[
                source_conn_resource,
                target_conn_resource
            ]
        )
    },
)