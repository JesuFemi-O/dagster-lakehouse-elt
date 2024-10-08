from dagster import Definitions
from dagster_iceberg.etl import definitions as elt_defs

defs = Definitions.merge(
    elt_defs.defs
)