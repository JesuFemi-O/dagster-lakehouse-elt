from setuptools import find_packages, setup

setup(
    name="dagster_iceberg",
    packages=find_packages(exclude=["dagster_iceberg_tests"]),
    install_requires=[
        "dagster==1.8.10",
        "dagster-embedded-elt==0.24.10",
        "dagster-pipes==1.8.10",
        "dagster-cloud==1.8.10",
        "dlt[dremio]"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
