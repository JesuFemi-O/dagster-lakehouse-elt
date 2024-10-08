CREATE SCHEMA iceberg.example_s3_schema WITH (location = 's3://warehouse/test');

CREATE TABLE iceberg.example_s3_schema.employees_test
(
  name varchar,
  salary decimal(10,2)
)
WITH (
  format = 'PARQUET'
);

INSERT INTO iceberg.example_s3_schema.employees_test (name, salary) VALUES ('Sam Evans', 55000);