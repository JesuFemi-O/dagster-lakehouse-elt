from dagster import Definitions, load_assets_from_modules
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_embedded_elt.sling import SlingResource
from dagster_iceberg.etl.dlt import assets as dlt_assets
from dagster_iceberg.etl.sling import assets as sling_assets

# add sling assets to the list too when you have them.
all_assets = load_assets_from_modules([dlt_assets, sling_assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "dlt": DagsterDltResource(),
        "sling":SlingResource()
    },
)