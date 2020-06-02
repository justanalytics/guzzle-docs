---
id: parameter_external
title: Guzzle Activity Type (formerly Job Config) – External
sidebar_label: Guzzle Activity Type (formerly Job Config) – External
---


## Guzzle Module - External

These are external frameworks and tools that are supported by Guzzle,

**Gobblin**

**ETL/ELT Tools**

ETL or ELT tools like ODI and Informatica can be integrated with Guzzle.

**Data Prep tools**

Data prep tools like Paxata, DataIKU, Trifacta, Data Mere can be orchestrated and hooked as external module

## Module Sections

### External (formerly known as Config)
This section will have properties as below,

* `Datastore` (formerly known as Endpoint)
* `Script`
* `Configure Lineages`

### Lineage
This section will have properties as below,

* `Lineages`

## Tags

* Tags are very useful to apply filters in Guzzle web UI
* You can enter multiple tags for single job. For example, `ext` `hr` `employee`
* If you apply filter based on more than one tag then filter criteria is treated as OR condition. Means all the jobs matching either of the tag filter will be displayed in the result. For example, if tag filter is applied on tag `ext` and `hr` then all jobs which has any one or both of this tag will be displayed in result