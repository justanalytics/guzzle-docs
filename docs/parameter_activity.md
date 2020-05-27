---
id: parameter_activity
title: Guzzle Activity (formerly Job Configs) Overview
sidebar_label: Guzzle Activity (formerly Job Configs) Overview
---


Guzzle Data Integration workbench is a on-premise as well as cloud-based data integration solution that automates the movement and transformation of data. It allows to quickly create, deploy, and monitor data ingestion, processing, reconciliation, data quality and house-keeping job. Guzzle supports sourcing and transforming data of various formats from wide array of sources including: files, cloud storage services, REST API, and JDBC, and write the results in to multiple types of targets. The transformed data can then be consume by BI and analytics tools, and other applications to drive business insights.

In Guzzle, there are 6 modules to define your Activities (formerly known as Job Configs).

- You can ingest data to target platform using **Ingestion** module
- You can transform data by processing complex business rules using **Processing** module
- You can perform recon between source and target tables and logs recon results into RDBMS using **Recon** module which can be readily consumed by data governance reports
- You can perform very granular level housekeeping on your target tables as per your data retention policy across various data storage layers within data lake using **Housekeeping** module.
- You can apply constraints check on crucial data attributes and log its results into RDBMS using **Constraint Checks** module
- You can execute any external job like for example running a shell script, powershell script, ADF pipeline, Databricks Notebook etc. using **External** module

Please refer below wikipages to read more details about each of the Guzzle job module,

   1. [ Ingestion ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-Ingestion)

   1. [ Processing ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-Processing)

   1. [ Recon ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-Recon)

   1. [ Constraint Checks ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-Constraint-Checks)

   1. [ Housekeeping ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-Housekeeping)

   1. [ External ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Activity-Type-(formerly-Job-Config)-%E2%80%93-External)