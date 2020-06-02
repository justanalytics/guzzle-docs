---
id: Arch_Guzzle_Core
title: Guzzle Core
sidebar_label: Guzzle Core
---


## Guzzle Core (or Internal) Modules

These are series of modules achieve specific workflows/ tasks for data integration. While they leverage the services/ context from Common services - they are supposedly to be fairly independent and can be run standalone. Native modules are loosely coupled and all the context is passed to this module with series of parameters (you can assume it passing a hash-map with key value of pairs)

### Ingestion

1. Caters to ingesting data from files, and relational database in batch mode and from Kafka in real-time mode
1. Performs schema validation, control checks, file format check
1. Allows configuring target partition scheme and incremental extraction criteria
1. Staleness handling for late arriving files
1. Supports end of day/end of month handling, overwrite and append modes on target

### Data Processing

1. A generic data loading framework which allows defining the transformation and loading rules using declarative config
1. Data Processing rules defined as SQLs
1. Enforces consistent implementation of standards and design patterns
1. Prevent rewriting repetitive ETL code and avoid any manual errors due to this
1. Allows to control performance and other relevant global parameters centrally

### Housekeeping

1. Generic module to house keep the data
1. Allows configuring the housekeeping based on date columns as well as other
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

These are external frameworks and tools that are supported by Guzzle,

### Gobblin

### ETL/ELT Tools

ETL or ELT tools like ODI and Informatica can be integrated with Guzzle.

### Data Prep tools

Data prep tools like Paxata, DataIKU, Trifacta, Data Mere can be orchestrated and hooked as external module