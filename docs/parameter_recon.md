---
id: parameter_recon
title: Guzzle Activity – Recon
sidebar_label: Guzzle Activity – Recon
---


## Guzzle Module - Recon

1. Recon framework for technical recon between source and target datasets
1. Performs count, hash and sum checks
1. Maintain detail list of record (PK values/ rowid) having reconciliation gaps

## Module Sections
### Source
This section will have properties as below,
- `Datastore` - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Primary Keys` - Specify primary key columns to be logged into `recon_detail` table if constraint check fails for a record. You can specify upto 10 columns if it is a composite primary key.
- `Table`
   * `Table` - Specify source table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
   * `Filter` - Specify record filters to be applied on source table, if any.
- `SQL`
   * `SQL` - Specify custom SQL to be executed on source datastore. For example, you may want to apply transformation rules. You can perform complex joins and apply data transformation rules to derive columns within custom SQL.
- `Configure Target Dependency` - This property is used to manually specify source table dependency and to manually configure Apache Atlas lineage.

### Target
This section will have properties as below,
- `Datastore` - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Primary Keys` - Specify primary key columns to be logged into `recon_detail` table if constraint check fails for a record. You can specify upto 10 columns if it is a composite primary key.
- `Table`
   * `Table` - Specify target table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
   * `Filter` - Specify record filters to be applied on source table, if any.
- `SQL`
   * `SQL` - Specify custom SQL to be executed on target datastore. For example, you may want to apply transformation rules. You can perform complex joins and apply data transformation rules to derive columns within custom SQL.

### Recon
This section will have properties as below,
- `Grouping Columns` - Specify columns to be used for grouping source data and target data for aggregating metrics to be compared between source and target for recon. For example, department_id.
- `Execute On Source` - Specify if you want to push down the source and target SQL queries along with filters to be applied on respective source and target endpoints for execution. Only aggregation and result comparison would be performed by Guzzle using Spark dataframe.
- `Recon Metrics` - Specify your recon metrics under this section. You can specify source aggregation column and target aggregation column which will be compared and recon results will be stored in Guzzle repository table `recon_summary` and `recon_detail`. For example, sum(salary).

> **Please note that, if reconciliation results between source and target doesn't match then Guzzle recon job is marked as FAILED and results are recorded in `recon_summary` and `recon_detail` metadata repository tables. When reconciliation results between source and target matches then Guzzle recon job is marked as SUCCESS and results are recorded in `recon_summary` table only.**

### Tags
- Tags are very useful to apply filters in Guzzle web UI
- You can enter multiple tags for single job. For example, `recon` `hr` `employee`
- If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `recon` and `hr` then all jobs which has any one or both of this tag will be displayed in result
