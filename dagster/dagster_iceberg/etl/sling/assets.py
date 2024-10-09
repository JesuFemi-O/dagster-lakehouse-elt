from dagster_embedded_elt.sling import sling_assets, SlingResource
from dagster_iceberg.etl.sling.sources.customers import replication_config

@sling_assets(replication_config=replication_config)
def sling_etl_assets(context, sling: SlingResource):
    yield from sling.replicate(context=context)
    for row in sling.stream_raw_logs():
        context.log.info(row)