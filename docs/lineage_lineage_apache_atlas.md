---
id: lineage_lineage_apache_atlas
title: Guzzle – Lineage (Apache Atlas)
sidebar_label: Guzzle – Lineage (Apache Atlas)
---

## Apache Atlas Lineage

Guzzle provides an integrated governance platform underpinned by Apache Atlas to serve the data lineage, governance, classification and cataloging needs. 
- Apache Atlas reads metadata for jobs defined in Guzzle and builds state of the art visual lineage which is very powerful feature to help understand end-to-end data processing pipeline. 
- Its comprehensive metadata lineage capabilities helps data engineers to perform impact analysis if there are any changes to be introduced for datasets used within data pipeline.
- Atlas Provides centralized metadata repository for hosting technical metadata for Data Lake, source systems of data lake including transaction systems, EDW and data mart (Oracle and SQL Server). 
- All the data integration jobs defined in Guzzle shall be integrated with Apache Atlas to provide auto population of technical metadata.
- Apache Atlas uses a local spark to generate all the dependencies across the tables.

![Apache_Atlas_Lineage](/guzzle-docs/img/docs/Apache_Atlas_Lineage.png)

## Recommendations

There are few recommendations to be followed for building complete lineage and to avoid any breakages in between due to some coding practices (as **Atlas lineage is a design time construct and not runtime construct**),

1. There is a tendency to define generic job template to ingest data for multiple tables as most of Guzzle Ingestion job and few of Processing job definition would be consistent across the jobs. Please note that, creating and using generic job template in Guzzle breaks the Apache Atlas auto-lineage feature available in Guzzle. Generic job template saves your time to define and maintain multiple job definitions, but that's the price you pay as you will have to configure Altas lineage manually for generic job templates - where job source and target information is passed through runtime parameters.

1. Atlas lineage is built properly if your logical endpoint, database name and table name is consistent across the layers. For example all sources and targets are translated to `<logical endpoint>.<database name>.<table name>`. If your logical endpoint name is lo_delta, database name is stg_hr and table name is employee in your activity, pipeline (formerly job config and job group respectively) then this translates to `lo_delta.stg_hr.employee` in Atlas. Make sure your tables are referred in this fashion all across your Guzzle code to maintain lineage.

1. You may want to parameterize database name and use parameter as a table prefix instead of hard-coding database name into your code. It is recommended to define database parameter and its value under Guzzle Environment as parameters defined under Environment gets resolved with its actual values while building the Atlas lineage. For example: `${p_env_stg_hr}.employee` where parameter `p_env_stg_hr` and its value `stg_hr` is defined under Guzzle Environment.

1. DO NOT use views or pre-sql or post-sql option available in Guzzle to embed your data transformation rules along with joins. Guzzle won't read tables used within views or pre-sql or post-sql to build the Atlas lineage and lineage will stop simply at your view name as what's inside view is unknown to Atlas lineage building process. Your data transformation rules along with joins should be written in SQL option provided to write custom SQL queries. If you have repeated code-block which you may want to re-use then use WITH clause in SQL section where you write your custom SQL query.

1. It is recommended not to use inconsistent character cases for table names used across the activities, pipelines (formerly known as job configs and job group respectively) like either maintain uppercase or lowercase all over to refer your tables. Though in recent Guzzle version Atlas lineage has become case insensitive.

1. It is also recommended not to use backticks (`) for table names used across the activities, pipelines (formerly known as job configs and job group respectively). Though in recent Guzzle version cleansing of backticks (if any) has already been handled.

1. Use of wild-char is also not supported in a file name if your source is a file.

## Manual Lineage for Reusable Job Template

As we discussed about using reusable/generic Guzzle job template under recommendation section above, Atlas lineage will not be derived automatically from such a template job configuration yaml and hence you will have to provide lineage metadata manually in `./conf/atlas.yml` file which can be located under Guzzle home directory.

There are two variations in manually providing Atlas lineage for a template job,
1) To create source, target and process node for each set of parameters. For example, `job1` in below sample yaml
2) To create source and target for each set of parameters and generate single process node. For example, `job2` in below sample yaml


```yaml
job_configs:
  job1:
    job_parameters:
      job1_IN:
        src_table: customers_IN
        tgt_table: customers_IN_tgt
      job1_SG:
        src_table: customers_SG
        tgt_table: customers_SG_tgt
  job2:
    merge_process_node: true
    parameters:
      - src_table: orders_IN
        tgt_table: orders_IN_tgt
      - src_table: orders_SG
        tgt_table: orders_SG_tgt
```

## Atlas Metadata Refresh and Reset

> **<<Refresh these contents to specify steps for Guzzle 2.0 UI>>**

### Metadata Refresh
- Open Guzzle UI and go to Job Configs
- At top middle of page, click button `SYNC ATLAS METADATA`
- This action will start metadata refresh if Atlas is configured correctly. It will take approx 5-10 minutes to sync Atlas metadata depending on # of Guzzle jobs to be synced

### Metadata Reset
- Go to Atlas installation directory and navigate at - `./apache-atlas-2.0.0/hbase/bin` to execute below commands, 
   * Execute - `hbase shell`
   * Execute - `disable 'apache_atlas_janus'`
   * Execute - `drop 'apache_atlas_janus'`
   * Execute - `disable 'apache_atlas_entity_audit'`
   * Execute - `drop 'apache_atlas_entity_audit'`
- Go to Atlas installation directory and navigate at - `./apache-atlas-2.0.0/bin`
- Stop atlas applications by executing - `atlas_stop.py`
- Start atlas applications by executing - `atlas_start.py`
- Go to Guzzle installation home directory and navigate at - `./guzzlescripts`
- Create atlas types by executing - `create-atlas-types.sh`
- This will reset your Atlas metadata and you can follow previously mentioned metadata refresh steps to re-populate atlas metadata

