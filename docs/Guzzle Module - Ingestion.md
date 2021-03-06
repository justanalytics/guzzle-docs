---
id: fundamentals_ingestion
title: Guzzle Module - Ingestion
sidebar_label: Guzzle Module - Ingestion
---

## Guzzle Module - Ingestion

It is focused to bring data inside the data lake (or target platform). This layer does not deal with complex processing logic. It can read data from heterogeneous sources and bring it into common target platform. Ingestion module should be used when the data movement is from heterogeneous database. Example: from Delta lake to SQL Warehouse or SQL server. It can apply validation, transformation and define rejection criteria for data before it is ingested into data lake.

> **"Bringing data in" is the primary concern of Ingestion module.**

1. It can read data from files, cloud storage services, REST API, RDBMS, HDFS, Hive, SQL server, Azure Synapse, JDBC sources etc.

1. Performs schema validation, control checks, file format check

1. Allows configuring target partition scheme and incremental extraction criteria

1. It is recommended to use prefix "jb_" while defining your job name followed by target database name and tables name. For example: jb_\<target database\>_\<table name\>_\<[description]\> like `jb_stg_hr_employee`

1. In validation and transformation section, you can define your row level validation rules and also map your additional control columns to be maintained into target

1. As ingestion job is meant for data movement between heterogeneous sources and target, you are not supposed to implement your business transformations rules in this job type.

1. Note that, when working with header-less source file, its best to put the column mapping in the source section instead of using transformation section to map col1 -> first_name and so forth. This enables following :
   * allows to do the sampling with proper column name
   * Ensure transformation section is use for real transformation like concating first name and last name (and not col1 and col2)
   * When not using column-mapping in source section, the source data frame will be hvae col1,col2,... and first_name,last_name.. which results in the auto crate to have double the column

1. Operations supported for target load are - `append`, `overwrite`

## Apache Atlas Lineage

There are few recommendations to be followed for building complete lineage and to avoid any breakages in between due to some coding practices,

1. There is a tendency to define generic job template to ingest data for multiple tables as Ingestion job definition would mostly be consistent across the jobs. Please note that, creating and using generic job template in Guzzle breaks the Apache Atlas auto-lineage feature available in Guzzle. Generic job template saves your time to define and maintain multiple job definitions, but that's the price you pay as you will have to configure Altas lineage manually for generic job templates - where job source and target information is passed through parameter.

1. Atlas lineage is built properly if your logical endpoint, database name and table name is consistent across the layers. For example all sources and targets are translated to `<logical endpoint>.<database name>.<table name>`. If your logical endpoint name is lo_delta, database name is stg_hr and table name is employee in your activity, pipeline (formerly job config and job group respectively) then this translates to `lo_delta.stg_hr.employee` in Atlas. Make sure your tables are referred in this fashion all across your Guzzle code to maintain lineage.

1. You may want to parameterize database name and use parameter as a table prefix instead of hard-coding database name into your code. It is recommended to define database parameter and its value under Guzzle Environment as parameters defined under Environment gets resolved with its actual values while building the Atlas lineage. For example: `${p_env_stg_hr}.employee` where parameter `p_env_stg_hr` and its value `stg_hr` is defined under Guzzle Environment.

1. DO NOT use views or pre-sql or post-sql option available in Guzzle to embed your data transformation rules along with joins. Guzzle won't read tables used within views or pre-sql or post-sql to build the Atlas lineage and lineage will stop simply at your view name as what's inside view is unknown to Atlas lineage building process. Your data transformation rules along with joins should be written in SQL option provided to write custom SQL queries. If you have repeated code-block which you may want to re-use then use WITH clause in SQL section where you write your custom SQL query.

1. It is recommended not to use inconsistent character cases for table names used across the activities, pipelines (formerly known as job configs and job group respectively) like either maintain uppercase or lowercase all over to refer your tables. Though in recent Guzzle version Atlas lineage has become case insensitive.

1. It is also recommended not to use backticks (`) for table names used across the activities, pipelines (formerly known as job configs and job group respectively). Though in recent Guzzle version cleansing of backticks (if any) has already been handled.

1. Use of wild-char is also not supported in a file name if your source is a file.


## Module Sections

### Source
- Depending on source datastore selection, you will have few properties readily available for use. These properties will vary based on your datastore selection. For example, if you select file datastore and delimited file format, you will get following properties to set,
   * `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from the drop-down (as appropriate). If connection is not available in drop-down then you have to create new
   * `Format` - Choose any of the supported file format (as appropriate) from given drop-down.
   * `File Pattern` - Specify directory name and full source file name (if name is static) or file name pattern (if name partly contains dynamic contents like date etc). For example: `hr/employee.csv` or `hr/employee_*.csv`. It also supports groovy expression, for more details please refer [Groovy Expression](https://gitlab.ja.sg/guzzle/docs/-/wikis/Groovy-expression-to-manipulate-Guzzle-Parameters). Guzzle can also traverse through the sub-directories under "hr/" directory, if you specify hr/\*\*/employee.csv or hr/\*\*/employee_*.csv. Here \/\*\*\/ is interpreted as to traverse from all the sub-directories under "hr/" directory and read all files matching file name pattern. You can also use parameter and pass its value during runtime.
   * `Character Set` - Specify character set of the contents of source file. For example: UTF-8.
   * `Column Delimiter` - Specify column delimiter used in source file.
   * `Quote Delimiter` - Specify, if source file contains text qualifier like double quote or single quote.
   * `Escape Character` - Specify, if source file contains any escape character.
   * `Contains Headers` - Specify, if source file contains a column header row.
   * `Infer Schema` - Specify, if you want to infer schema from the source file.
   * `Clean Column Name` - Specify, if source file column name contains spaces or any other characters which you may want to clean. Guzzle will remove specified characters automatically.
   * `Multi-Line` - Specify, if source file contains row split due to carriage returns.
   * `Add Column Mapping` - Manually specify source to target column mapping if source column names and target column names doesn't match or source file doesn't contain column header row.
   * `Include Source File Name As Column` - Specify, if you want to include source file name as one of the Guzzle mapped column like src_filename, src_control_filename.
   * `Configure Process Path` - Specify, if you want to move source files to some other directory once they are successfully processed. It is quite useful when you want to archive successfully processed files by moving them into some other directory.
   * `Configure Control File Settings` - Specify, if you have a control file for your source file which contains row count and you want Guzzle to do row count check with control file before file can be processed.
   * `Partial Load` - Specify, if you want Guzzle to load partial set of files into target when there is more than one file matching source file pattern. For example, if there are 10 files matching source file pattern available at source file directory and 2 files fails control check validation or any other validation defined then `Partial Load` will allow job to load other 8 files into target table, if this property is enabled.

- If you select relational or JDBC datastore, you will get following properties to set,
   * `Table`
      * `Table` - Specify source table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
      * `Filter` - Specify record filters to be applied on source table, if any.
   * `SQL`
      * `SQL` - Specify custom SQL to be executed on source datastore. For example, you may want to use column alias to match source column names with target column names or want to apply some basic transformation rules. Please note that, it is not recommended to perform complex joins or data transformation as part of the ingestion module job. Once data is ingested from source to target platform, processing module jobs are best suited for performing those activities.
   * `Pre SQL` - Specify any Pre-SQL you may want to execute before reading source table or executing source custom SQL. For example, refresh index, collect stats etc.
   * `Post SQL` - Specify any Post-SQL you may want to execute after reading source table or executing source custom SQL. For example, drop table, delete file etc.
   * `Configure Watermark` - 
      * `Partition Column Name`
      * `Watermark Columns`
      * `Watermark Filter`
   * `Configure Columns Restriction`
      * `Include Columns` - Specify what all source columns you want to map to target table. If columns to be included is less than columns to be excluded list.
      * `Exclude Columns` - Specify what all source columns you don't want to map to target table. If columns to be excluded is less than columns to be included list.
   * `Configure Table Dependency` - 

### Validation And Transformation
This section will have properties as below,
- `Strict Datatype Check` - 
- `Inherit Columns and Datatype` -  
- `Global Discard` - Specify, if you want to route the records failed validation into reject table and stop them from loading into target. If enabled, then records which failed validation rule won't be loaded into target table and such records would be routed and loaded into reject table specified under reject section. If not enabled, records which failed validation gets loaded into target table as well as reject table.
- `Columns` - Specify column validation or transformation rules under this section. You can define primary key check, not null check, data type check and custom validation SQL for each source column under this section. You can also define column transformation SQL under this section.

### Target
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Table` - Specify target table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
- `Pre SQL` - Specify any Pre-SQL you may want to execute before loading target table. For example, truncate table tablename, drop index indexname etc.
- `Post SQL` - Specify any Post-SQL you may want to execute after loading target table. For example, collect stats, create index indexname etc.
- `Auto Create Table` - Specify, if you want Guzzle job to auto-create target table if table is not existing.
- `Operation` - Specify, if you want to perform append or overwrite operation target table by selecting a given option from drop-down.
- `Configure Truncate Partition Columns` - Specify target table partition columns and their corresponding values to truncate target table partition before target load. Truncate partition column values can also be passed as a parameter.


### Reject
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Failure Threshold (%)` - Specify failure threshold as in % of total source records. If record rejection % count breaches specified threshold % then Guzzle job fails and nothing is written into target table.
- `Table` - Specify reject table name. It is recommended to name your reject table as `rej_<target table name>`. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
- `Pre SQL` - Specify any Pre-SQL you may want to execute before loading reject table. For example, truncate table tablename, drop index indexname etc.
- `Post SQL` - Specify any Post-SQL you may want to execute after loading reject table. For example, collect stats, create index indexname etc.
- `Auto Create Table` - Specify, if you want Guzzle job to auto-create reject table if table is not existing.

#### Ingestion job has Reject handling at different levels

* File checksum level
* Row level validations
* Rejection threshold in %

##### Rejection target as File
If you are using reject target as a file then you can log rejected records with following information,
1. All columns that are intended to be loaded in reject file
1. Additional column to capture comma separate error messages

##### Rejection target as table
If you are using reject target as a table then you can log rejected records with following information,
1. All columns that are intended to be loaded in target + partition clause as specified for reject target
1. Additional column to capture comma separate error messages

### Tags
- Tags are very useful to apply filters in Guzzle web UI
- You can enter multiple tags for single job. For example, `stg` `hr` `employee`
- If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `stg` and `hr` then all jobs which has any one or both of this tag will be displayed in result

## Sample YAML Config

Following is the sample ingestion job yaml configuration for csv source and hive target

```yaml
job:
    type: ingestion
    failure_threshold: 20
    partial_file_load: false

source:
    endpoint: users_base_path
    source_schema_derivation_strategy: source
    properties:
        source_file_pattern: ${location}/${system}/users.*.csv
        format: delimited
        charset: UTF-8
        format_properties:
            column_delimiter: ","
            contains_header: true
        control_file:
          extension: ctl
          path: /control-files/${environment}/${location}/${system}
        processed_file_path: /processed/${environment}/${location}/${system}

schema:
    strict_schema_check: true
    filter_sql: "name like 'user%' and age > 23 or name in (select name from ${endpoint.users_db}.test)"
    columns:
        id:
            primary_key: true
            data_type: INT
            nullable: false
        name:
            data_type: CHAR(10)
            validate_sql: "@ in (select name from ${endpoint.users_db}.test)"
            transform_sql: "case when @ in (select name from ${endpoint.users_db}.test) then @ else 'None' end"
        age:
            data_type: DECIMAL(2,0)
            validate_sql: "@ > 25"
        created_time:
            validate: false

target:
    endpoint: users_db
    columns_to_be_loaded: common
    partition_columns:
      system:
        value: ${system}
      location:
        value: ${location}
    properties:
        table: ${database_name}.${users_table}
```

In above sample job configuration two types of placeholders can be used:

* **${job_parameter_name}** : Value for such expression will be resolved by parameters we pass while invoking job
* **${endpoint.logical_endpoint_name}** : Value for such expression will be resolved by getting database name property from physical-endpoint of given logical-endpoint and environment

### Additional Details
* **type** will be used by common service (orchestration) to identify which type of job to be triggered
* **failure_threshold** is used to specify number of invalid records(in percentage) allowed while processing single file. If threshold reaches, whole file is considered to be discarded and no records from that file will be processed
* When multiple files are present in the source and failure threshold is reached for some of the files, **partial_file_load** is used to specify whether to process the remaining files or discard all the source files. Default value is false which means all the files will be discarded if threshold is reached in a single source file


**Support for parameter in above sample yaml**

* In source section:  
  1. source_file_pattern  
  1. control_file >> path  
  1. processed_file_path
* In schema section:  
  1. validate_sql  
  1. transform_sql
* In target section:  
  1. partition_columns  
  1. table
