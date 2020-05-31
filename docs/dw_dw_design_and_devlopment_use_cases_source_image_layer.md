---
id: dw_dw_design_and_devlopment_use_cases_source_image_layer
title: Source Image Layer
sidebar_label: Source Image Layer
---

### Source Image Layer

This is a logical data layer hosted on Data lake. The structured datasets shall be defined as Hive tables for on-premise or Databricks Delta tables for azure cloud setup while unstructured data will be hosted as files on HDFS or Azure Blob storage account. Additional technologies like HBase and Elasticsearch shall be considered to host real time event data or machine data for future requirements. The key characteristics of source image layers are:

* Provides one-stop landing area for all the enterprise datasets – providing uniform access platform for all the downstream needs ranging from MIS, analytics or downstream system consumption.
* At most fundamental grain – same as source and full set of source attributes
* One to one copy of source data with audit trail and support for historical snapshot (allows to retrieve the month end views for downstream processing at latter point)
* Applies fundamental integrity checks like data type validation, custom validation checks, reject handling and error logs
* Addresses atomic transformation and basic cleansing like trimming or normalizing the values to units (in case if they come in thousands)
* Keeps audit trail in case of multiple re-run and re-pull of data from source (interim copies of data)
* Caters to structure, semi-structured and unstructured data
* Built in assurance framework – using technical reconciliation and control checks module in Guzzle
* Daily to near Realtime batch – supports flexibility to change the refresh frequency from every few seconds to daily or monthly
* Un-blocked: Straight through processing in to this layer without any dependency on whether downstream has consumed data
* Zero data-modelling - one to one copy of all the relevant dataset from source system – providing complete source image for all current and future data needs
* Supports consolidation (or alignment) of similar source datasets (having same semantics and granularity). This allows for simpler downstream consumption. Example Policy data from three different systems can be stacked up in same source image layer table if they have common subset attributes and similar granularity
* Supports Incremental loading (either using timestamp columns on source or integrating with other CDC tools available at customer)