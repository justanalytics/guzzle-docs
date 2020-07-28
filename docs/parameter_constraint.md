---
id: parameter_constraint
title: Guzzle Activity Type (formerly Job Config) – Constraint Checks
sidebar_label: Guzzle Activity Type (formerly Job Config) – Constraint Checks
---


## Guzzle Module - Constraint Checks

1. Perform Data Quality (DQ) validation on specified columns and tables
1. Logging of records and statistics failing the constraint checks
1. The validation rules applicable for structured data and can currently be specified as SQL

## Module Sections

### Source
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Primary Keys` - Specify primary key columns to be logged into `constraint_check_detail` table if constraint check fails for a record. You can specify upto 10 columns if it is a composite primary key.
- `Grouping Columns` - Specify grouping columns in source table if source data has to be aggregated before performing constraint check. All grouping column names and values are logged into `constraint_check_summary`, `constraint_check_detail` tables if constraint check fails for a record. You can specify upto 10 columns for group by to perform aggregation.
- `Table`
   * `Table` - Specify source table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
   * `Filter` - Specify record filters to be applied on source table, if any.
- `SQL`
   * `SQL` - Specify custom SQL to be executed on source datastore. For example, you may want to apply transformation rules. You can perform complex joins and apply data transformation rules to derive columns within custom SQL.
- `Configure Table Dependency` - This property is used to manually specify source table dependency and to manually configure Apache Atlas lineage.

### Constraint Checks
This section will have options to set as below,
- **`Validation Rules`** - You can specify constraint checks to be performed on source table under this section.
   * **`Name`** - Specify a name for validation rule. For example, 
      1. employee_name_not_null_check
      1. dept_id_domain_value_check
   * **`Sql`** - Specify validation sql which should evaluate to `TRUE` if record passes the constraint check. Records which doesn't qualify the rule specified under this option are logged into `constraint_check_summary`, `constraint_check_detail` tables. 
      For example,
      1. employee_name is not null
      1. dept_id in (10,20,30,40,50,60)
      1. salary > 1000 
   * **`Constraint Data`** - Specify list of columns for which additonal data to be logged into `constraint_check_summary`, `constraint_check_detail` tables. For example,
      1. employee_id||'~'||employee_name||'~'||
      1. employee_id||'~'||employee_name||'~'||dept_id
      1. employee_id||'~'||employee_name||'~'||salary

### Tags

* Tags are very useful to apply filters in Guzzle web UI
* You can enter multiple tags for single job. For example, `ck` `hr` `employee`
* If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `ck` and `hr` then all jobs which has any one or both of this tag will be displayed in result
