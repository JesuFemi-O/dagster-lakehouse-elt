commands I executed:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install dagster-embedded-elt
pip install paramiko
pip install s3fs

export PATH=/Users/emmanuelogunwede/code_space/open_source/dagster-lakehouse-elt/venv/bin:$PATH

dagster project scaffold --name dagster_iceberg

cd dagster
pip install -e ".[dev]"

```

dremio password => TestPassword123


- first step is to create your virtual env

- install the dagster requirements

- pip install your dagster project in dev mode

- run your docker-compose up -d

- next step is to connect nessie & minio to dremio

- start your dagster server

- run the dlt pipeline

- run the sling pipeline

- check minio to see the files, query via trino & dremio

i ran this to do the etl from sftp to trino:

```bash
sling run \
--src-conn LOCAL_SFTP \
--src-stream 'customers_100.csv' \
--tgt-conn TRINO \
--tgt-object 'target_schema.target_table' \
--mode full-refresh
```