from dagster_embedded_elt.dlt import DagsterDltResource, dlt_assets
from dagster_iceberg.etl.dlt.sources import fake_coy_elt

from dagster import AssetExecutionContext


@dlt_assets(
    dlt_source=fake_coy_elt.fake_coy_source,
    dlt_pipeline=fake_coy_elt.pipeline,
    name="fake_coy",
    group_name="api_source",
)
def dlt_api_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)