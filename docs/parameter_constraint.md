---
id: parameter_constraint
title: Guzzle Activity Type (formerly Job Config) – Constraint Checks
sidebar_label: Guzzle Activity Type (formerly Job Config) – Constraint Checks
---


## Guzzle Module - Constraint Checks

1. Perform Data Quality (DQ) validation on specified columns and tables
1. Logging of records and statistics failing the constraint checks
1. The validation rules applicable for structured data and can currently specified as SQL

## Module Sections

### Source
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Primary Keys` - **\<<Add contents here\>>**
- `Grouping Columns` - **\<<Add contents here\>>**
- `Table`
   * `Table` - Specify source table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
   * `Filter` - Specify record filters to be applied on source table, if any.
- `SQL`
   * `SQL` - Specify custom SQL to be executed on source datastore. For example, you may want to apply transformation rules. You can perform complex joins and apply data transformation rules to derive columns within custom SQL.
- `Configure Table Dependency` - **\<<Add contents here\>>**

### Constraint Checks
This section will have properties as below,
- `Validation Rules` - **\<<Add contents here\>>**

### Tags

* Tags are very useful to apply filters in Guzzle web UI
* You can enter multiple tags for single job. For example, `ck` `hr` `employee`
* If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `ck` and `hr` then all jobs which has any one or both of this tag will be displayed in result