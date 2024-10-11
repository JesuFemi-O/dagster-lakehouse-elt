# Dagster ELT Lakehouse

![architecture](/docs/assets/dag-lakehouse.png)

This repo demonstrates how to use dagster's elt framework to develop an elt platform for an iceberg powered lakehouse

# How to run

1. Clone this repository to your local machine
```bash
git clone https://github.com/JesuFemi-O/dagster-lakehouse-elt.git
```

2. cd into the project root directory
```bash
cd dagster-lakehouse-elt
```

3. create a virtual environment and setup the environment variables using make
```bash
make lakehouse-setup
```

This command creates the virtual environment if it doesn't exist, installs the requirements and creates the env files on the first run of the command. on subsequent runs it only checks and skips the install if the setup conditions are satisfied.

4. open the env file at ./dagster/.env and fill it
    - DESTINATION__FILESYSTEM__BUCKET_URL: This is the bucket dlt will stage files in before writing it to iceberg tables.
    - DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID: The AWS access key which we have already configured to `minio` in the docker-compose file.
    - DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY: The AWS secret key which we have already configured to be `minio123` in the docker-compose file.
    - DESTINATION__FILESYSTEM__CREDENTIALS__ENDPOINT_URL: since we are using Minio which is an s3 compatible storage in place of S3, we have to set this value to a URL that let's us call the minio API
    - DESTINATION__DREMIO__STAGING_DATA_SOURCE: This can be the name of your connection in DREMIO to AWS S3 (minio in our case) whatever you name the S3 source connection is the value you provide here.
    - DESTINATION__DREMIO__CREDENTIALS__DATABASE: This is the name used to configure the connection to Nessie in dremio
    - DESTINATION__DREMIO__CREDENTIALS__PASSWORD: The dremio account password
    - DESTINATION__DREMIO__CREDENTIALS__USERNAME: The dremio account username
    - DESTINATION__DREMIO__CREDENTIALS__HOST: The dremio host which can be set to `localhost` in our setup.
    - DESTINATION__DREMIO__CREDENTIALS__PORT: The port we have binded to the dremio's container port
    - SLING_HOME_DIR: This value helps us to manage our sling connections using the env.yaml approach.
    - SLING_TRINO_CONNECTION_URL: The sling trino URL
    - SLING_SFTP_CONNECTION_URL: The sftp connection URL

5. open the env file at ./infra/.sling/env.yaml and provide the connection credentials. the values should be the values below since they're managed via the docker-compose and the values at ./infra/sftp/users.conf:
```yaml
connections:
  SFTP_CONN:
    type: sftp
    host: localhost
    password: password1
    port: "2222"
    user: user1
  
  TRINO_CONN:
    type: trino
    http_url: http://trino:@localhost:8080?catalog=iceberg&schema=customers

variables: {}
```

Trino is configured to not require a password and so you the url only contains the username.

6. start the lakehouse services
```bash
make lakehouse-init

```

7. Open dremio in your web browser `http://0.0.0.0:9047/` and sign up, ensure the username and password used, matches the values you set in your `DESTINATION__DREMIO__CREDENTIALS__USERNAME` and `DESTINATION__DREMIO__CREDENTIALS__PASSWORD` env values.
![dremio_signup_paage](/docs/assets/00-dremio-signup.png)

8. Create a connection to nessie. ensure your connection name is the same as the value for `DESTINATION__DREMIO__CREDENTIALS__DATABASE` in your `.env`
![nessie_general_tab](/docs/assets/03-nessie-general-view.png)

    - ensure that the authentication is set to None
    - set the endpoint url to `http://nessie:19120/api/v2`
    - in the storage tab, set the storage provider to AWS
    - set authentication method to AWS Access Key
    - set AWS Access and Access Secret keys to the values you configured for `DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID` and `DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY` whcih should match the values in the minio service environment variable values in the docker-compose file.
    - for the connection properties in the storage tab, set the following values:
        - fs.s3a.path.style.access : True
        - fs.s3a.endpoint : minio:9000
        - dremio.s3.compat : true
    - uncheck the `encrypt connection` checkbox

![storage-provider](/docs/assets/04-storage-provider.png)

![storage-config-properties](/docs/assets/05-storage-connection-properties.png)

click Save and this should connect dremio to Nessie.

9. Create connection to Minio in dremio
    - ensuure the connection name is same as the value of `DESTINATION__DREMIO__STAGING_DATA_SOURCE` env variable, it is how dlt knows what source to reference for object storage in dremio
    - set authentication method to AWS Access Key
    - set AWS Access and Access Secret keys to the values you configured for `DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID` and `DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY` whcih should match the values in the minio service environment variable values in the docker-compose file.
    - uncheck the `encrypt connection` checkbox
    - enable compatibility mode
    - set the root path to `/` 
    - set the default CTAS format to `ICEBERG`
    - add the following connection properties:
        - fs.s3a.path.style.access : True
        - fs.s3a.endpoint : minio:9000

![storage-properties](/docs/assets/07-storage-advanced-properites.png)

![storage-properties-advanced](/docs/assets/08-storage-advanced-config.png)

click save.

10. start the dagster server
```bash
make lakehouse-serve
```

11. open dagster at `http://127.0.0.1:3000/` which should land you on the default view, the click on view global assets lineage on the top right corner and click on matrialize all to run both sling and dlt 

![dagster-asset-default](/docs/assets/09-asset-default.png)

![dagster-asset-global](/docs/assets/10-asset-global-view.png)

on materializing all assets and viewing the run, you should get a result simillar to the one in the image below:

![dagster-success](/docs/assets/11-dagster-run-success.png)

you can now query your iceberg tables in dremio

![nessie-coy](/docs/assets/13-nessie-fake-coy.png)

![nessie-customers](/docs/assets/12-nessie-customers.png)

![nessie-query-iceberg](/docs/assets/14-nessie-iceberg-query.png)


## Exploring incremental load behavior
The fake coy api has an endpoint that allows you update random companies information which can then allow you to incrementally update records in your lakehouse. you can visit the api docs in the api [readme](/fake_coy_api/readme.md) or via its swagger docs at `http://localhost:8000/`


## Conclusion
This project serves as a simple proof of concept that can be built upon to devlop a fully production ready lakehouse, you can explore the docs of the tools leveraged in this project to build upon the ideas shred here.

Resources

- [dlthub](https://dlthub.com/)
- [slingdata](https://slingdata.io/)
- [dremio](https://www.dremio.com/)
- [trino](https://trino.io/)
- [nessie](https://projectnessie.org/)
- [dagster](https://docs.dagster.io/getting-started)
- [minio](https://min.io/docs/minio/container/index.html)
