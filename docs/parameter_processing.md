---
id: parameter_processing
title: Guzzle Activity Type (formerly Job Config) – Processing
sidebar_label: Guzzle Activity Type (formerly Job Config) – Processing
---


## Guzzle Module - Processing

It is focused to transform data already ingested into data lake (or target platform). This layer deals with complex processing logic by implementing all data transformation rules. And this transformation can usually cut across multiple tables (via join/ sub-query etc), multiple records (aggregate/ grouping), multiple columns (multi column case statements) or even link up source and target data to do update or insert of source data into target table. Data Processing is the module which supports intra-ETL from staging to foundation and finally to analytics data tables.

> **"Transforming data from one form to other" is the key purpose of Data Processing module.**

1. It is a generic data loading framework which allows defining the transformation and loading rules using declarative config

1. Data Processing rules defined as SQLs

1. Enforces consistent implementation of standards and design patterns

1. Prevent rewriting repetitive ETL code and avoid any manual errors due to this

1. Allows to control performance and other relevant global parameters centrally

1. It can read data from RDBMS, Hive, SQL server, Azure Synapse, other JDBC sources etc.

1. It is recommended to use prefix "jb_" while defining your job name followed by target database name and tables name. For example: jb_\<target database\>_\<table name\>_\<[description]\> like `jb_fnd_hr_employee`

1. In additional columns section, you can map your additional control columns to be maintained into target. You can also map framework generated SCD type 2 columns to your SCD type 2 target dimension.

1. As processing job is meant for data movement between homogeneous sources and target, you can not read data from source table maintained in one technology and write it into target table maintained into some other technology.

1. Rich set of operations supported for target load are - `append`, `delete`, `effective date merge`, `merge`, `overwrite`, `update only`

## Framework Generated Columns

In this job type, you will have set of framework generated columns readily available in **Additional Columns** section,

- w_created_business_ts
- w_created_ts
- w_refresh_ts
- w_current_record_flag
- w_eff_start_date_ts
- w_eff_end_date_ts
- w_sequence_key
- w_version_key


## Apache Atlas Lineage

There are few recommendations to be followed for building complete lineage and to avoid any breakages in between due to some coding practices,

1. There is a tendency to define generic job template to ingest data for multiple tables as few processing job definition would be consistent across the jobs. Please note that, creating and using generic job template in Guzzle breaks the Apache Atlas auto-lineage feature available in Guzzle. Generic job template saves your time to define and maintain multiple job definitions, but that's the price you pay as you will have to configure Altas lineage manually for generic job templates - where job source and target information is passed through parameter.

1. Atlas lineage is built properly if your logical endpoint, database name and table name is consistent across the layers. For example all sources and targets are translated to `<logical endpoint>.<database name>.<table name>`. If your logical endpoint name is lo_delta, database name is fnd_hr and table name is employee in your activity, pipeline (formerly job config and job group respectively) then this translates to `lo_delta.fnd_hr.employee` in Atlas. Make sure your tables are referred in this fashion all across your Guzzle code to maintain lineage.

1. You may want to parameterize database name and use parameter as a table prefix instead of hard-coding database name into your code. It is recommended to define database parameter and its value under Guzzle Environment as parameters defined under Environment gets resolved with its actual values while building the Atlas lineage. For example: `${p_env_fnd_hr}.employee` where parameter `p_env_fnd_hr` and its value `fnd_hr` is defined under Guzzle Environment.

1. DO NOT use views or pre-sql or post-sql option available in Guzzle to embed your data transformation rules along with joins. Guzzle won't read tables used within views or pre-sql or post-sql to build the Atlas lineage and lineage will stop simply at your view name as what's inside view is unknown to Atlas lineage building process. Your data transformation rules along with joins should be written in SQL option provided to write custom SQL queries. If you have repeated code-block which you may want to re-use then use WITH clause in SQL section where you write your custom SQL query.

1. It is recommended not to use inconsistent character cases for table names used across the activities, pipelines (formerly known as job configs and job group respectively) like either maintain uppercase or lowercase all over to refer your tables. Though in recent Guzzle version Atlas lineage has become case insensitive.

1. It is also recommended not to use backticks (`) for table names used across the activities, pipelines (formerly known as job configs and job group respectively). Though in recent Guzzle version cleansing of backticks (if any) has already been handled.

## Module Sections

### Source
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Incremental` - **\<<Add contents here\>>**
- `Table`
   * `Table` - Specify source table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
   * `Filter` - Specify record filters to be applied on source table, if any.
- `SQL`
   * `SQL` - Specify custom SQL to be executed on source datastore. For example, you may want to use column alias to match source column names with target column names or want to apply transformation rules. You can perform complex joins and apply data transformation rules to derive columns within custom SQL as part of the processing module job.
- `Pre SQL` - Specify any Pre-SQL you may want to execute before reading source table or executing source custom SQL. For example, refresh index, collect stats etc.
- `Post SQL` - Specify any Post-SQL you may want to execute after reading source table or executing source custom SQL. For example, drop table, delete file etc.
- `Configure Table Dependency` - **\<<Add contents here\>>**
- `Additional Columns` - Specify, if you want to map any additional framework generated columns (as listed earlier on this page) or derived column to target table.

### Target
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Table` - Specify target table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
- `Operation` - Specify, if you want to perform append, overwrite, merge, effective date merge, update only or delete operation on target table by selecting a given option from drop-down.
- `Template` - Specify, Guzzle template to be used like delta, default, sqlserver or delta_v2 to perform target operations by selecting a given option from drop-down.
- `Pre SQL` - Specify any Pre-SQL you may want to execute before loading target table. For example, truncate table tablename, drop index indexname etc.
- `Post SQL` - Specify any Post-SQL you may want to execute after loading target table. For example, collect stats, create index indexname etc.
- `Primary Keys` - Specify primary key columns list from target table to uniquely identify record, if target operation is any of merge, update only, effective date merge or delete.
- `Merge Columns` or `History Columns` - Specify merge columns to be updated into target table, if target operation is merge or update only. Specify history columns list to maintain history into SCD Type 2 target, if target operation is effective date merge. You can use this option in conjunction with framework columns `w_eff_start_date_ts`, `w_eff_end_date_ts`, `w_sequence_key`, `w_version_key` available in Additional Columns source section by mapping them into target table.
- `Truncate Partition Columns` - Specify target table partition columns and their corresponding values to truncate target table partition before target load. Truncate partition column values can also be passed as a parameter.
- `Soft Delete` - Specify, if you want to perform soft delete onto target table where flag column can be maintained into target table to identify if record is active or deleted. Use this option in conjunction with one of framework column `w_current_record_flag` available in Additional Columns source section by mapping it to target table.

### Tags
- Tags are very useful to apply filters in Guzzle web UI
- You can enter multiple tags for single job. For example, `fnd` `hr` `employee`
- If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `fnd` and `hr` then all jobs which has any one or both of this tag will be displayed in result

## Ingestion vs Processing
* Ingestion should be used when the data movement is from heterogeneous database. Example: from  Delta lake to SQL Warehouse or to SQL server
* Data movement across same database can be done via processing job type.
* When building csv -> parquet file -> external table in hive and the loading to Aggregate will not generate the linage in Atlas - Ideally one should do :CSV -> Delta or Hive tables -> Aggregate
* For scenarios like taking incremental data from lake (hive, delta, files on adls) and merging to dim table in  SQL Server (or any JDBC target) following options are possible in the order of preference:
   * This ideally be achieved by keeping the dim table in data lake first, merging the data in lake and moving / mirroring the table to SQL server or Azure Synapse.
   * If the data volume is huge and merge touches small set of record then the incremental data should be copied over to staging table in SQL Server and then do merge using ETL.
   * Another option (which only works for selected scenario) is to create external table in SQL Server or Azure Synapse using the incremental data available in lake and then by doing merge.
* It ideal to leverage onto data processing capabilities of Databricks - and hence it is better to generate aggregates in Databricks and copy over (only impacted partitions)