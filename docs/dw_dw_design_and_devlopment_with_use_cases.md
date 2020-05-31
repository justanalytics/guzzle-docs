---
id: dw_dw_design_and_devlopment_with_use_cases
title: DW Design and Development Best Practices with Use Cases
sidebar_label: DW Design and Development Best Practices with Use Cases
---

[[_TOC_]]


## Background

Data lakes are different from DWH and data marts in manyways - look at this: https://medium.com/@rpradeepmenon/demystifying-data-lake-architecture-30cf4ac8aa07


## Overview
![image](/guzzle-docs/img/docs/image.png)


Data lake has source image at the heart of it - wihch is the purest form of data. But further to it, you can have reusable curated datasets and use-cases speicfic dataset.
Some guidelines around this are:

### Source Systems 
- This refers to full array of sources both structured and unstructured for an enterprise and are available for directly loading in to Data lake
- The data from these systems shall be interfaced via direct DB connection (using JDBC), flat files or API. 
- Future extension allows the real-time integration of events from this system using the message queue infrastructure like Kafka. 
- Support for both incremental and full load of data from the sources.
### Source Image Layer
This is a logical data layer hosted on Data lake. The structured datasets shall be defined as Hive tables while unstructured data will be hosted as files on HDFS. Additional technologies like HBase and Elasticsearch shall be considered to host real time event data or machine data for future requirements.
The key characteristics of source image layers are:
- Provides one-stop landing area for all the enterprise datasets – providing uniform access platform for all the downstream needs ranging from MIS, analytics or downstream system consumption. 
- At most fundamental grain – same as source and full set of source attributes
- One to one copy of source data with audit trail and support for historical snapshot (allows to retrieve the month end views for downstream processing at latter point)
- Applies fundamental integrity checks like data type validation, custom validation checks, reject handling and error logs
- Addresses atomic transformation and basic cleansing like trimming or normalizing the values to units (in case if they come in thousands) 
- Keeps audit trail in case of multiple re-run and re-pull of data from source (interim copies of data)
- Caters to structure, semi-structured and unstructured data
- Built in assurance framework – using technical reconciliation and control checks module in Guzzle
- Daily to near Realtime batch – supports flexibility to change the refresh frequency from every few seconds to daily or monthly 
- Un-blocked: Straight through processing in to this layer without any dependency on whether downstream has consumed data
- Zero data-modelling - one to one copy of all the relevant dataset from source system – providing complete source image for all current and future data needs
- Supports consolidation (or alignment) of similar source datasets (having same semantics and granularity). This allows for simpler downstream consumption. Example Policy data from three different systems can be stacked up in same source image layer table if they have common subset attributes and similar granularity
- Supports Incremental loading (either using timestamp columns on source or integrating with other CDC tools available at customer) 
### Reusable datasets 
This is processed and enriched data layer in Data lake holding primarily structured datasets post the first level of sanitation and consolidation done in the source image layer and further standardization to it. The key characteristics of source interdependent data layer is as follows:
- Governed datasets abstracting wider user community from the complex source system ETL logic and source system subject matter expertise.
- Hosts fundamental and commonly re-usable data sets implementing commonly used transformation and derivation. Example: transposing the rows to column where required, stamping final code values like Address Type, Customer type after handling source system specific logic or translating transaction system customer ids to standard set of customer id. 
- Applies requisite precedence logic to determine most authority source for particular attributes or data sets. Example source image layer may contain multiple sources of customer data. The Source independent data layer provides finalized customer dataset merging information from multiple sources
- Does consolidation and alignment of multiple disparate dataset have similar business meaning
- Not a big-bang approach: Caters to gradual and incremental extension of model
- Use right level of normalization – Has a tolerance of some level of redundancy across the datasets however necessary recon and control should be in place. 
- In order to keep the dataset and transformation more manageable, the set of attributes at a given grain shall be broken into multiple tables where required. Example: Customer demographics, customers aggregated transaction profile and aggregated custom service experience attributes can be structured as three datasets
- Maintain historical snapshots of transformed data
- Serves to MIS and needs of data scientist looking for more consolidated and streamlined datasets as their starting point
- Depending on the complexity and usage of the datasets, this layer can be implemented as set of database views, providing agility to implement extensions.
- Depending on whether the composite datasets are deriving generic set of attributes, the same can be made available in public area where users with relevant access are able to leverage
- These datasets should be built in conjunction of SME of business processes owning the data, IT teams from source systems, data architects team and analytics users

### Analytics and Access data layer
This layer is meant to create final datasets which are more focused and use case specific 
- Contextual dataset for specific use-cases and reporting needs. Data model may undergo constant refactoring for this.
- May keep historical snapshot based on consumption requirement
- Taps on to Source image layer and source independent layer to create requisite use-case specified dataset
- Specific computation, aggregation, derivation and snapshot catering to particular reporting need – example: dataset compliance reporting or input dataset for customer churn model
- Leverages appropriate tools to host the data (graph storage, no-sql (Elasticsearch or HBase), or relational/hive)

2.1.5	End user data exploration area 
- A sandbox area in Data lake for user to explore the data within the Data lake or bring any additional data from the internal sources that are not part to of Data lake yet or external sources
- This is defined as separate “write” schema created in Data lake to allow selected users or departments to perform following:
o	Upload or source additional datasets
o	To query existing data in Data lake and blending with additional datasets uploaded by users
o	To build derived data sets and configure them as standalone scripts or Guzzle jobs
- User can use Zeppelin notebook or any desktop SQL tools supporting JDBC connectivity
- The data exploration area is sandboxed for each user or user groups (with read or write access) to only that database (and folder). Users cannot further grant the access this sandboxes to other user group providing more centralized access control.
- All the compute and memory resources will be drawn from users assigned resource queue. This insulates the BAU batch jobs and other system workload from end user data exploration activities.

### End user data exploration area 
- A sandbox area in Data lake for user to explore the data within the Data lake or bring any additional data from the internal sources that are not part to of Data lake yet or external sources
- This is defined as separate “write” schema created in Data lake to allow selected users or departments to perform following:
- Upload or source additional datasets
- To query existing data in Data lake and blending with additional datasets uploaded by users
- To build derived data sets and configure them as standalone scripts or Guzzle jobs
- Two write areas shall be defined as part of the project – one for an individual user and other for a group of user. 
- User can use Zeppelin notebook or any desktop SQL tools supporting JDBC connectivity
- The data exploration area is sandboxed for each user or user groups (with read or write access) to only that database (and folder). Users cannot further grant the access of this sandboxes to other user group providing more centralized access control.
- All the compute and memory resources will be drawn from users assigned resource queue. This insulates the BAU batch jobs and other system workload from end user data exploration activities.
Note: Considering there was no usage for adhoc adhoc load and need of sanbox hence the separate user, HDFS folder and Yarn Queue was NOT defined 
### Data Governance, Classification and Cataloguing
The solution proposes an integrated governance platform underpinned by Apache Atlas and Apache Ranger to serve the data governance, classification and cataloging needs. 
- Atlas Provides centralized metadata repository for hosting technical metadata for Data Lake, source systems of data lake including transaction systems, EDW and data mart (Oracle and SQL Server). 
- All the data integration jobs defined in Guzzle shall be integrated with Apache Atlas  to provide auto population of technical metadata.


## Staging Design

At times staging tables needs to maintain multiple copies of the incoming data. This happens in following cases:
1. Data is loaded from same system multiples times and only latest copy is to be maintained in the final data lake tables
1. There are errors in the source data forcing repull -in this case original copy of source data should be retained for any tractability including downstream impact it may have created including user reports (which with latest data may show different)


## Layers in Data flow
This also refers to stages in data pipelines


## Audit Columns
Audit columns in data tables are the most crucial items
Guzzle encourages that data lakes implement standard naming convetion of Audit columns for better readability and troubleshooting by both product support and development team alike.


Recommended Audit columns that

### General Guidance

### Recommended Audit column names

Sr.|Audit Column name|Purpose|Guzzle parameter/transformation|Partitioned Column|Applicable to which data layer | comments
---|---|---|---|---|---|---
*|w_refresh_ts|||||




## Table naming convention

## References
1. https://medium.com/@rpradeepmenon/demystifying-data-lake-architecture-30cf4ac8aa07
