---
id: recorded_training_sessions
title:Recorded Training Sessions
sidebar_label: Recorded Training Sessions
---



|Sr.No.|Topic|Description|Sample data|Other Details|
|---|---|---|---|---|
1| What is Guzzle?|intro of guzzle modules and other details|none|none|
1| Config as Code|why config as code is better - consistent, faster, concise|none|none
1| Introducing Guzzle UI|walk through key modules of Guzzle UI - mainly focus on Guzzle job UI, and viewing runtime audits|none|none
1| Ingest Delimited files|Supports local and hdfs; supports wild card file names; file header and header-less file are handled|flights; files with multi line data|none
1| Ingest Fixed format files|loading data from delimited file where certain values can be skipped, overlapping data in two fields|aircraft makes master|none
1| Query run-time Audits and Logs|different work units as separate steps, publishing steps as separate, provenance of the config and what not|none|none
1| Ingest data from JDBC source|Handling of data types, schema, excluding selected columns and rows without writting whole SQL|airports|none
1| Incrementally loading data from JDBC source|how the water marking works, how full/incremental works to over-ride existing water marks|airports|none
1| Ingest data from API source|supports API key, |holiday API|none
1| Setup logical and physical data connections|Abstracting physical connection information from Guzzle config naturally allows to keep the Guzzle config portable across the environment. User refer to the logical end point names in the job configs. A logical data end point is mapped to specific instance of physical config  via a mappig called "environment" config|none|none
1| Ingest JSON and XML files|to take multi structured json file with single line doc or multi line; how to use nested element to map to a table; how multi value can be loaded as concat string||none
1| Introducing user-defined parameters|Introducing user define parameters and how they can be referred in the configs. Options of making table name, file name etc dynamic.||none
1| Doing Data Transformation during ingestion|single column transform and multi column transform, using place holder/parameters, the support manipulation of Apache log file using reg-ex, simple use case of masking data or hashing, concating column, using place holder in parameters and referring to other param or config table containing list of values||none
1| Manipulating File name when loading data|how a file name filed can be used for advance usecase when doing ingestion including stamping the file name in the data sets and extracting valid business info from file names like date or country|flights|none
1| Do Schema validation: Data Type, Uniqueness, non-null checks|How to perform wide array of schema checks during ingestion and how the data gets logged into the DQ tables; introduce the threshold percentage, DQ tables and files; handling of multi errors in file; discard or non-discard; error threshold
1| Custom validations when ingesting data| show custom validation for a given column and across columns (lke arr_time > dep_time; allowing to refer static values from another table as SQL to avoid hard-coding|flights|none
1| Loading data in to partitioned Hive tables|working with partitioned table is the typical usecase of storing data for given data tranche in separate partition for ease of rerun, house keeping, tractability, downstream consumption and administration. How the source columns, fixed values and user parameters can be used when speechifying destination partition where the data gets loaded. Also how the auto-create of the table honours the partition data types|flights|none
1| Control file check|how to perform control file checks in Guzzle - stress that this is after the filters applied, it supports taking control file from diff location and with diff extension. Handling of control file check across multiple files and rejecting all the flies or partial
1| Transforming data in Hive tables using SQL| supports truncate/insert; append; merge
1| Update/insert in Hive tables| cover merge, partial merge 
1| Advance Update/insert in Hive tables| Framework columns , incremental data from the source, soft-delete
1| Recon between tables| how to reconcile the data between staging and downstream table within hadoop. How it can produce the counts and sum checks at certain granularity, how to view the data , how to drill-down ; how multiple recon are kept as separate rows etc
1| Drill-down Recon between tables across database| how recon is supported across database and option on whether to do the counts and group by query at the source and bring only the data final summary data over. Emphasis on how to make the recon parametric so that it can be run with different data. 
1| Check constraint| To perform critical data monitoring including validation of the values, loggin the count for each rule failure, how the checks are across columns. With SQL based source the check constraint can be across the tables
1| Check constraint on Source| Performing check constraint on source, supporting drill-down
1| House-keeping Hive tables| Performing house-keeping of tables on date column partition ; different policy; moving the data to secondary table instead of purging (it will  replace partitions secondary table)
1| House-keeping advanced scenarios| Strict house keeping at the month end or take the last available month - granularity at which strick checks are performed; dynamic table names and usage of place holder; how 
1| Creating data load batches | Guzzle supports concept of Job batches which can be used to run group of Guzzle jobs; Defining the batches, stages, job groups, passing source parameters
1| Advance batch handling scenario| Batch init with skipping certain dates options; rerun capability for a particular batches;stages pairing; logging run-time audits|none|none
1| Creating data load batches | Guzzle supports concept of Job batches which can be used to run group of Guzzle jobs; Defining the batches, stages, job groups, passing source parameters
1| Dependency management scenario| Advance  dependency management scenario across systems and batches; |none|none
1| Advance user context parameters| Advance parameter scenario in Guzzle and real-usecase for them |none|none
1| Atlas integration| The Atlas integration for different job types, handling of dynamic tables names , file based sources and performing lineage
1| Lineage and impact analysis  in Atlas| The Atlas integration on how to find the tables dependency based on SQL, 
1| Airflow Integration| Trigger individual jobs and batches from Atlas. How Atlas can provide much needed scheduling , throttling, dependency management framework on top of Guzzle (same can be expanded to Control-M and other tools)
1| Metadata extractor utility| Guzzle supports advance metadata which can be ext
1| Metadata Search| Guzzle supports free text search of entire metadata to help find out needed jobs loading particular targets
1| Deep dive of Guzzle runtime logs
1| Rest API to manipulate Guzzle  metadata| how guzzle provides three key interface to build metadata: direct editing of JSON, REST API and User Interface. The video compares three options and guidance  on which option is better
1| Introduction to streaming| Introduces Guzzle stream configuration and how it allows to define the data pipeline to process the messages on Kafka topic. The config allows to define DAG and multi step logic to process streaming data including validation, logging data  in Hbase or Hive; displaying it on screen
1| Processing network events| This video takes through an approach of processing custom event and apply string of transformation including SQL lookup, reg-exp, validation etc
1| Applying custom transformation to streams| how to do advance transformation of the raw data
1| Loading data from log flies|  Show how Apache and few other logs files can be processed
1| Loading data Salesforce| Processing data from salesforce - different entity , how it can be scheduled
1| Ingesting live streams from twitter|Ingesting data from live streams of Twitter and building real time dashboard using PBI
1| Deploy guzzle on Azure Data Bricks| how to deploy guzzle on Azure Data bricks and using varoius services to work through the data
1| End to end ETL on Azure Data Bricks| Full set of scenarios on Guzzle
1| Setup the Git repository and ssh keys
1| Advanced incremental loading data from JDBC source|airports, other table explaining water-marking by systems or country from global tables and partitioning|none|none
1| Guzzle How to:Setup of Guzzle |loading data from JDBC source|airports, other table explaining water-marking by systems or country from global tables and partitioning|none|none
1| CI/CD|How to run the full end to end CI/CD pipeline for Guzzle projects. This deploys the  binaries and configs in fresh env and does required clean-up|none|none
1| Test Automation|How to do the test automation of ETL jobs and ensure the functionality is as per expected - for both  business rules and also the configs are behaving as per expected |none|none
1| Running regressions and test Automation using Guzzle's Recon framework|How to use the recon frmework to build a recon of end to end data pipelines ensuring all the auto checks are performed post the data load|none|none
1| Setting up Guzzle repository in different database types|Guzzle has support for multiple databsae types for hosting the repository|none|none
1| Importing parent config|Guzzle provides unprecedented re-usability via using importing parent config. With Guzzle taking YAML as the metadata format, it provides allows user to encapsulate the most common configs centrally including end point names, standard DQ checks and audit columns to be loaded






