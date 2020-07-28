---
id: compute_spark_runtime
title: Guzzle - Spark Runtime
sidebar_label: Guzzle - Spark Runtime
---

## Spark Environment

Spark is the core compute used for all the Guzzle Activity modules except External Activity module which could differ based on its configuration.

1. Ingestion module is all-and-all spark, raw data is directly read into spark for files/JDBC/APIs/queues and later written to sink (from spark). Even elastic search available in Guzzle web UI uses native connectors provided by spark.
1. ELT pattern is supported for Processing module - where a SQL is generated (INSERT INTO...SELECT or MERGE INTO ..) and submitted to Databricks
1. Recon has push down optimization to generate and send summary query to DQ
1. Check constraint brings raw data as per source SQL/table into spark and generates DQ metric there in spark. Plan is to have support for push down for this in future for JDBC end points as well.
1. Housekeeping - today only supports Hive and Delta - but eventually when it starts supporting JDBC, it will do push down (its in road map)

## Spark Configuration for On-premise setup
### Configure Local Spark
In op-premise Guzzle setup, you can configure local spark to execute your workloads. Though Guzzle allows to use local spark for running lighter jobs, this configuration of spark won't be able to leverage on entire spark cluster compute resources and hence it is recommended to use Yarn spark cluster for heavier workloads.

As seen in below sample configuration, you can set number of executors, driver memory limit, executor memory limit and if environment is Kerberized then set additional argument `--properties-file /guzzle/conf/spark_hdp_310.conf`. 

![Spark_Runtime_1](/guzzle-docs/img/docs/Spark_Runtime_1.png)

File `spark_hdp_310.conf` should have Application ID keytab file name along with its location. Here Application ID is the one used for executing Guzzle workloads like jobs/job groups/batch/stage. This file should also have Kerberos principal details mentioned as below.

```
spark.yarn.keytab /guzzle/conf/<<Application ID>>.keytab
spark.yarn.principal <<Application ID>>@<<Kerberos Principal>>.LOCAL
```

### Configure Yarn Spark Cluster
In op-premise Guzzle setup, you can configure YARN spark cluster to execute your workloads. This configuration of spark will be able to leverage on entire spark cluster compute resources and hence it is recommended to use Yarn spark cluster for heavier workloads.

As seen in below sample configuration, you can set number of executors, driver memory limit, executor memory limit, driver classpath, executor classpath and if environment is Kerberized then set additional argument `--properties-file /guzzle/conf/spark_hdp_310.conf`. 

![Spark_Runtime_2](/guzzle-docs/img/docs/Spark_Runtime_2.png)

File `spark_hdp_310.conf` should have Application ID keytab file name along with its location. Here Application ID is the one used for executing Guzzle workloads like jobs/job groups/batch/stage. This file should also have Kerberos principal details mentioned as below.

```
spark.yarn.keytab /guzzle/conf/<<Application ID>>.keytab
spark.yarn.principal <<Application ID>>@<<Kerberos Principal>>.LOCAL
```

## Spark Configuration for Cloud setup (Azure Cloud)
### Configure Azure Databricks

In Guzzle azure cloud setup, you can use databricks to execute your workloads. There are 3 types of databricks clusters available in Guzzle.

### Azure Databricks Cluster Types

#### Data Analytics

Data Analytics cluster is recommended for interactive queries along with concurrent user support. This cluster type is configurable in Guzzle and it can also execute the workloads, but it is not recommended to use it for your BAU data loads. Since Data Analytics cluster is costlier than Data Engineering cluster for per DBU usage and meant for interactive queries through Databricks notebook in shared environment where multiple people have to collaborate as a team.

Here is sample configuration in Guzzle for Data Analytics cluster if at all you want to use one,

![Spark_Runtime_3](/guzzle-docs/img/docs/Spark_Runtime_3.png)

#### Data Engineering

Data Engineering cluster is recommended for automated workloads. It is recommended to use it for your BAU data loads.

Here is sample configuration in Guzzle for Data Analytics cluster,

![Spark_Runtime_4](/guzzle-docs/img/docs/Spark_Runtime_4.png)

Note that, you shall setup below custome spark configuration only when your Databricks workspace is using external hive metastore, otherwise these properties can be ignored.

```
spark.hadoop.javax.jdo.option.ConnectionDriverName com.microsoft.sqlserver.jdbc.SQLServerDriver
spark.hadoop.javax.jdo.option.ConnectionURL jdbc:sqlserver://guzzlesqlserver.database.windows.net;database=adb_hive_metastore_db;encrypt=true;trustServerCertificate=true;create=false;loginTimeout=30
spark.databricks.delta.preview.enabled true
spark.hadoop.javax.jdo.option.ConnectionUserName {{secrets/guzzlemetastore/guzzle-metastore-user}}
datanucleus.fixedDatastore false
spark.hadoop.javax.jdo.option.ConnectionPassword {{secrets/guzzlemetastore/guzzle-metastore-pwd}}
datanucleus.autoCreateSchema true
spark.sql.hive.metastore.jars builtin
spark.sql.hive.metastore.version 1.2.1
```

![Spark_Runtime_5](/guzzle-docs/img/docs/Spark_Runtime_5.png)

![Spark_Runtime_6](/guzzle-docs/img/docs/Spark_Runtime_6.png)

#### Data Engineering Light

Data Engineering Light cluster is even cheaper than Data Engineering cluster for per DBU usage. Once you select this type, rest all the other configuration for this cluster type would be same as Data Engineering cluster. 

Note that, Data Engineering Light provides a runtime option for jobs that don’t need the advanced performance, reliability, or autoscaling benefits provided by the more capable Databricks Data Engineering cluster offering.

### Configuring Azure Databricks Scope and Azure Keystore
