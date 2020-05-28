---
id: version-0.7.26-docshome
title: What is Guzzle
sidebar_label: Introduction to Guzzle
original_id: docshome
---


## Key Drivers 
There are plethora of frameworks and data integration tools available for Big Data and traditional DWH usecases. The reason or if we can say motivation that we decided to put together Guzzle - a set of data integration frameworks, boils down to following:
1. To **make Big data technologies more accessible** and enable wider adoption for typical Data warehouse and data integration usecase. The idea is to simplify the implementation of data integration requirements of Data lake, make it faster, easy to manage, extend etc.
2. To **address the standard data integration and DWH patterns** that are usually not available as part of the native tools and standard frameworks. 

## What Guzzle is not
Guzzle is not meant to compete with existing Data Integration and ETL tools or existing ETL frameworks like Gobblin. Whilst it provides native modules to support Ingestion , Data processing, and others - it also supports calling the jobs / procs from other frameworks and ETL tools.


# Guzzle Architecture Overview
Guzzle is build as combination of foundation or common services , native modules and external modules which come together to provide integrated set of accelerators which can achieve [Guzzle's goal of RACE OIL] (Documentation/guzzle-overview#guzzle-goals-race-oil)
![image](/guzzle-docs/img/docs/guzzle_architecture.png)

## Common Services

### Job Dependency
1. Supports flexibility of defining dependency between different stages of data flow (staging, foundation, access layer)
1. Supports dependency of individual jobs within ETL stages
1. It passes appropriate context to allow concurrent loading of same target dataset
1. Tightly coupled with Data Load and Data Ingestion frameworks

### Runtime audit
1. Run time audit to maintain granular logs of individual jobs  and intermediate steps 
1. Row counts of successful, exception records processed, start/end time
1. Performance metrics like CPU, memory and IO usage by the data processing jobs
1. All audits captured in the context of system, country, data loading stage (staging, foundation etc), table for ease of reporting

### Data Endpoints
This is the abstractions for any data end points like local files, HDFS, RDBMS etc.


### System Paramters
This are global parameters which are determine during the invocation of the jobs

### User Parameters
This are additional paramters

### File Upload Tools
A generic tool to upload and stage the file in HDFS/Unix

### Watermarks and Control information
This deal with keeping the state of control information like last business date loaded for a given system/ country,. 

### Performance Monitoring
This deals with monitoring the granular resource usage on the cluster by various jobs



## Native (or Internal) Modules
This are series of modules achieve specific workflows/ tasks for data integration. While they leverage the services/ context from Common services - they are supposedly to be fairly independent and can be run standalone. Native modules are loosely coupled and all the context is passed to this module while series of parameters (you can assume it passing a hash-map with key value of pairs)

### Ingestion
1. Cateres to ingesting data from files, and relational database in batch mode and from Kafka in real-time mode
1. Performs schema validation, control checks, file format check
1. Allows configuring target partition scheme and incremental extraction criteria
1. Staleness handling for late arriving files
1. Supports end of day/month handling, merge, truncate insert and append modes on target

### Data Processing
1. A generic data loading framework which allows defining the transformation and loading rules using declarative config
1. Data Processing rules defined as SQLs
1. Enforces consistent implementation of standards and design patterns
1. Prevent rewriting common of the ETL code and avoid any manual errors due to this
1. Allows to control performance and other relevant global parameters centrally

### Housekeeping
1. Generic module to house keep the data 
1. Allows configuring the housekeeping based on date columns as well as others
1. Allows configuring retention period for multiple time periods (xxx rolling days , yy rolling month end etc.)
1. The data falling outside of retention window can be purged or moved to alternate location


### Constraint Check
1. Perform Data Quality (DQ) validation on specified columns and tables 
1. Logging of records and statistics failing the constraint checks
1. The validation rules applicable for structured data and can currently specified as SQL

### Recon and Tractability
1. Recon framework for technical recon between source and target datasets
1. Performs count, hash and sum checks
1. Maintain detail list of record (PK values/ rowid) having reconciliation gaps


## External Modules
This are external frameworks and tools that are supported by Guzzle.  

### Gobblin

### ETL/ELT Tools
ETL or ELT tools like ODI and Informatica can be integrated with Guzzle.

### Data Prep tools
Data prep tools like Paxata, DataIKU, Trifacta, Data Mere can be orchestrate and hooked as external module