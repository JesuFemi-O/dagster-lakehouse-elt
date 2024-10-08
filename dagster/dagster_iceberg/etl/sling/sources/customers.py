from dagster_embedded_elt.sling import SlingConnectionResource
from dagster import EnvVar

source_conn_resource = SlingConnectionResource(
    name="MY_SFTP",
    type="sftp",
    connection_string=EnvVar("SLING_SFTP_CONNECTION_URL")
)

target_conn_resource = SlingConnectionResource(
    name="MY_TRINO",
    type="trino",
    connection_string=EnvVar("SLING_TRINO_CONNECTION_URL")
)


replication_config = {
    "source": "MY_SFTP",
    "target": "MY_TRINO",
    "defaults": {"mode": "full-refresh", "object": "{stream_schema}_{stream_table}"},
    "streams": {
        "customers_100.csv": {"mode": "full-refresh", "object": "customers"},
    },
}



# @sling_assets(replication_config=replication_config)
# def my_assets(context, sling: SlingResource):
#     yield from sling.replicate(context=context)
