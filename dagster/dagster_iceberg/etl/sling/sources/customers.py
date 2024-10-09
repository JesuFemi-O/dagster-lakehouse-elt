from dagster_embedded_elt.sling import SlingConnectionResource
from dagster import EnvVar

source_conn_resource = SlingConnectionResource(
    name="SFTP_CONN",
    type="sftp",
    connection_string=EnvVar("SLING_SFTP_CONNECTION_URL")
)

target_conn_resource = SlingConnectionResource(
    name="TRINO_CONN",
    type="trino",
    connection_string=EnvVar("SLING_TRINO_CONNECTION_URL")
)


replication_config = {
    "source": "SFTP_CONN",
    "target": "TRINO_CONN",
    "defaults": {"mode": "full-refresh", "object": "{stream_schema}_{stream_table}"},
    "streams": {
        "customers_100.csv": {"mode": "full-refresh", "object": "customers"},
    },
}
