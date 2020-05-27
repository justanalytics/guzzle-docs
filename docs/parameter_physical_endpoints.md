---
id: parameter_physical_endpoints
title: Physical Endpoints
sidebar_label: Physical Endpoints
---


**Physical Endpoint** in Guzzle is physical host connection details stored to communicate with various Source or Target Systems.

**Currently supported** list of Guzzle physical endpoints are,
* Delta
* File
  * Amazon S3
  * Azure Data Lake Storage
  * DBFS
  * HDFS
  * LFS (Local File System)
* Google Analytics
* Hive
* JDBC
  * MySQL
  * Oracle
  * PostgreSQL
  * SQL Server
  * Manually Setup additonal JDBC
* Kafka
* Phoenix
* Rest
* Salesforce
* Shell

**Key considerations** while creating physical endpoints in Guzzle,
1. Decide the physical endpoints correctly as this is crucial on how you see grouping of Guzzle datasets in lineage. Ideally treat each data schema / or db name in hive/ schema in SQL server/ as separate physical endpoint even tough they are from same database and user for this endpoint is same. Likewise for files have separate endpoint for each container or directory which logically groups one data domain (example one system) - avoid using top level directory as that will force you to put sub-dir in file name pattern as hard-coded or via param - and such sub-dir might be env specific making job config either not portable across env or adds a additional param to be provided at run-time
1. Avoid relying on schema prefix as much possible when specifying source, target or SQL - this will ensure the jobs are portable across environments.
1. Having said that, you may still consider defining common endpoint if there are too many databases/schemas in your project and if it would be difficult to manage separate endpoint for each database/schema. Like for example, if tables are segregated using separate databases/schemas created for each data-mart where there would be multiple data-marts to support business reporting needs. In this scenario, database name can also be defined as Environment Parameter and this parameter name can be prefixed with table name in Guzzle Job Configuration without affecting job portability across environments.


**Naming Conventions**
* Prefix each physical endpoint with ph_ 
* Followed by technology for endpoint
* Followed by type/vendor for endpoint applicable for FILE/JDBC endpoits
* Followed by database instance or schema name or description

  `ph_<technology>_<type/vendor>_<database>`

For example,
1. ph_jdbc_oracle_dwhxxx
1. ph_file_hdfs_landing
1. ph_delta_dwhxxx