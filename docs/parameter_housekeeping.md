---
id: parameter_housekeeping
title: Guzzle Activity Type (formerly Job Config) – Housekeeping
sidebar_label: Guzzle Activity Type (formerly Job Config) – Housekeeping
---


## Guzzle Module - Housekeeping

You can perform very granular level housekeeping on your target tables as per your data retention policy across various data storage layers within data lake using this module.

## Module Sections

### Housekeeping
This section will have properties as below,
- `Datastore` (formerly known as Endpoint) - You can choose any of the available logical connection from drop-down (as appropriate). If connection is not available in drop-down then you have to create new.
- `Table` - Specify table name. You can also use parameter and pass its value during runtime. You may prefix your table name with database/schema name.
- `Housekeeping Column` - Specify column name to be used for housekeeping the table. Mostly this is going to be partition columns of the table.
- `Operation` - Delete, Move
- `Configure Table Dependency` - **\<<Add contents here\>>**
- `Reference Point` - Specify any of the available option in the drop-down list - `Current Time`, `Max Value`, `Value` as a reference point for applying the housekeeping rules. If selected `Current Time`, it will housekeep treating current system timestamp as a reference point to apply the housekeeping rules defined under Retention Strategies. If selected `Max Value`, it will calculate the maximum value for `Housekeeping Column` specified in above section as reference point. If selected `Value`, you can specify custom value or pass value through a runtime parameter as reference point for housekeeping.
- `Retention Strategies` - Specify retention strategies for housekeeping your table.
   * `Partitions`
   * `Retention Strategy`
   * `Day of Week`
   * `Strict Retention Period End`
   * `Strict Retention Grain`

### Tags

* Tags are very useful to apply filters in Guzzle web UI
* You can enter multiple tags for single job. For example, `hk` `hr` `employee`
* If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `hk` and `hr` then all jobs which has any one or both of this tag will be displayed in result