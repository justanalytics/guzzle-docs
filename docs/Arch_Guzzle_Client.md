---
id: Arch_Guzzle_Client
title: Guzzle Client
sidebar_label: Guzzle Client
---

There are 3 Guzzle client services for interacting with Guzzle core services.
1. Guzzle UI
1. Guzzle API
1. Guzzle CLI

Let's go through each of the Guzzle client service in details below.

## Guzzle UI

Guzzle Web UI is very user friendly web interface to author, execute and monitor Guzzle jobs. You can perform following activities using Guzzle Web UI,
- Create connections for reading/writing various technologies 
- Configure spark compute and environments
- Configure GIT for code version management
- Create jobs configurations for ingestion, processing, recon, housekeeping, constraint checks etc.
- Download job metadata
- Sync Atlas metadata for building lineage
- Define, execute and monitor batches
- User access management using different built-in Personas for access control
- Define workflow for manual file uploads for data ingestion

## Guzzle API

You with deal with Guzzle API call mostly if it is Guzzle cloud setup. There is detailed step by step guid available on how to integrate Guzzle API with Azure Data Factory (ADF) in Azure Cloud setup. Please refer wikipage here at - [ Call Guzzle from Azure Data Factory ](parameter_datafactory.md)

For various Guzzle API call, quick reference to syntaxes to be used are as follows,

### Call Guzzle REST API which triggers job group:
 
**Request Body**:

```json
{
  "system": "test",
  "location": "SG",
  "business_date": "2020-04-02 16:01:27",
  "guzzle.spark.name": "local1",
  "job_group": "USERS_INGESTION",
  "environment": "test2"
}
```

When we debug pipeline, we will get job instance id of triggered job group in response of API call (similar to job trigger API)

### Call Guzzle REST API which initializes a batch record:
  
**Request Body**:

```json
{
  "contextParams": {
    "system": "sp"
  },
  "businessDate": "2020-04-02 16:11:38",
  "environment": "test2"
}
```

When we debug pipeline, we will not get anything in response of the API call

### Call Guzzle REST API which initializes batch records for multiple days:
  
**Request Body**:

```json
{
  "contextParams": {
    "system": "sp",
    "location": "all"
  },
  "businessDateRange": {
    "startDate": "2020-04-02 16:00:00",
    "endDate": "2020-04-06 16:00:00"
  },
  "period": "1",
  "environment": "test2"
}
```

When we debug pipeline, we will not get anything in response of the API call

### Call Guzzle REST API which triggers a stage of the batch:
 
**Request Body**:

```json
{
  "param1": "value1",
  "system": "sp",
  "guzzle.spark.name": "local1",
  "stage": "STG",
  "environment": "test2"
}
```

When we debug pipeline, we will not get anything in response of the API call

### Call Guzzle REST API which triggers multiple stages of the batch:
  
**Request Body**:

```json
{
  "param1": "value1",
  "system": "sp",
  "guzzle.spark.name": "local1",
  "stage": "STG,FND,PLP",
  "environment": "test2"
}
```

When we debug pipeline, we will not get anything in response of the API call


## Guzzle CLI

You can use Guzzle CLI using one of shell script `guzzle.sh` located under `$GUZZLE_HOME/scripts` directory.

If you execute this script on $ prompt it will print the entire help for working with Guzzle CLI as seen below,

```sh
Usage: ./guzzle.sh [COMMAND]

    where COMMAND is one of:

    run
        use to run job or stages

        job
            to run adhoc guzzle job.
            usage: ./guzzle.sh run job job_name environment [parameters] [spark_config]

            ex. ./guzzle.sh run job transaction_csv_staging environment=prod "business_date=2019-01-01 00:00:00" param1=value1 param2=value2
                ./guzzle.sh run job transaction_csv_staging environment=prod job_instance_id=190315105226 "business_date=2019-01-01 00:00:00" param1=value1 guzzle.spark.num_executors=1 guzzle.spark.driver_memory=512m

            job_name        guzzle job name
                            ex. transaction_csv_staging
            environment     environment name
                            ex. environment=prod
            [parameters]    job parameters. it is specified in key=value format.
                            ex. job_instance_id=190315105226 location=SG system=transaction "business_date=2019-01-01 00:00:00" ...
            [spark_config]  used to overwrite default spark configuration. spark parameters are passed with "guzzle.spark" prefix
                            ex. guzzle.spark.num_executors=1 guzzle.spark.driver_memory=512m ...

        stage
            used to run stages.
            usage: ./guzzle.sh run stage environment context_params stage [parameters]

            ex. ./guzzle.sh run stage environment=prod system=transaction location=SG stage="STG,FND" param1=value1 param2=value2

            environment     environment name
                            ex. environment=prod
            context_params  context parameters. it is specified in key=value format.
                            ex. system=transaction location=SG ...
            stage           execution stages. multiple stages are separated by comma(,).
                            ex. stage="STG,FND"
            [parameters]    job parameters. it is specified in key=value format.
                            ex. location=SG system=transaction "business_date=2019-01-01 00:00:00" ...

        job_group
            used to run job group.
            usage: ./guzzle.sh run job_group job_group_name environment [parameters] [spark_config]

            ex. ./guzzle.sh run job_group asia_region_transactions environment=prod "business_date=2019-01-01 00:00:00" transaction_type=credit_card order_type=online guzzle.spark.name=spark_default

            job_group_name  job group name
                            ex. asia_region_transactions
            environment     environment name
                            ex. environment=prod
            [parameters]    job parameters. it is specified in key=value format.
                            guzzle.job_group.resume=y is used to resume execution from last failed job group run.
                            guzzle.job_group.partial=true is used to allow partially run job group.
                            ex. "business_date=2019-01-01 00:00:00" transaction_type=credit_card order_type=online ...
            [spark_config]  used to provide spark configuration profile.
                            ex. guzzle.spark.name=spark_default

    init
        use to initialize batch records or guzzle repository.

        batch

            used to initialize batch records for provided context column and date range.
            usage: ./guzzle.sh init batch environment context_params [[business_date] | [start_date] [end_date] [period]]

            ex. ./guzzle.sh init batch environment=prod system=transaction location=SG "business_date=2019-01-01 00:00:00"
                ./guzzle.sh init batch environment=prod system=transaction location=SG "start_date=2019-01-01 00:00:00" "end_date=2019-01-15 00:00:00" period=2

            environment     environment name
                            ex. environment=prod
            context_params  context parameters. it is specified in key=value format.
                            ex. system=transaction location=SG ...
            [business_date] initialized batch record for specific business date. do not forget to add double quotes("")
                            ex. "business_date=2019-01-01 00:00:00"
            [start_date]
            [end_date]      initialized batch records for specified date range. do not forget to add double quotes("")
                            ex. "start_date=2019-01-01 00:00:00" "end_date=2019-01-15 00:00:00"
            [period]        used to create periodic batch records for specified date range. it is used with start_date and end_date.
                            period\'s value is considered in days.
                            ex. period=2

        repository
            used to initialize guzzle repository or to generate repository script
            usage: ./guzzle.sh init repository environment [generate]

            ex. ./guzzle.sh init repository environment=prod
                ./guzzle.sh init repository environment=prod generate

            environment     environment name
                            ex. environment=prod
            [generate]      generate repository initialization script
                            ex. generate

    sync
        use to synchronize guzzle data

        atlas
            used to synchronize guzzle job and environment data with atlas
            usage: ./guzzle.sh sync atlas environment=prod

            ex. ./guzzle.sh sync atlas environment=prod

            environment     environment name
                            ex. environment=prod

    export
        use to export guzzle data.

        job_metadata
            used to export job config metadata.
            usage: ./guzzle.sh export job_metadata [job_type] [job_name] [target]

            ex. ./guzzle.sh export job_metadata
                ./guzzle.sh export job_metadata target=/home/user/guzzle_test/export
                ./guzzle.sh export job_metadata job_type=ingestion,processing target=/home/user/guzzle_test/export
                ./guzzle.sh export job_metadata job_name=transaction_csv_staging target=/home/user/guzzle_test/export

            [job_type]      job type. multiple job types are separated by comma(,)
                            ex. job_type=ingestion,processing
            [job_name]      job name. multiple job names are separated by comma(,).
                            ex. job_type=transaction_csv_staging
            [target]        target directory path. default it exports file in current directory.
                            ex. /home/user/guzzle_test/export

        column_metadata
            used to export column metadata.
            usage: ./guzzle.sh export column_metadata [job_type] [job_name] [target]

            ex. ./guzzle.sh export column_metadata
                ./guzzle.sh export column_metadata target=/home/user/guzzle_test/export
                ./guzzle.sh export column_metadata job_type=ingestion,processing target=/home/user/guzzle_test/export
                ./guzzle.sh export column_metadata job_name=transaction_csv_staging target=/home/user/guzzle_test/export


            [job_type]      job types. multiple job types are separated by comma(,)
                            ex. job_type=ingestion,processing
            [job_name]      job name. multiple job names are separated by comma(,).
                            ex. job_type=transaction_csv_staging
            [target]        target directory path.
                            ex. /home/user/guzzle_test/export
```