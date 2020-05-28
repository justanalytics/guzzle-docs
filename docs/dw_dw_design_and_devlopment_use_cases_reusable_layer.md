---
id: dw_dw_design_and_devlopment_usecases_reusable_layer
title: Reusable Layer
sidebar_label: Reusable Layer
---


This is processed and enriched data layer in Data lake holding primarily structured datasets post the first level of sanitation and consolidation done in the source image layer and further standardization to it. The key characteristics of source interdependent data layer is as follows:

* Governed datasets abstracting wider user community from the complex source system ETL logic and source system subject matter expertise.
* Hosts fundamental and commonly re-usable data sets implementing commonly used transformation and derivation. Example: transposing the rows to column where required, stamping final code values like Address Type, Customer type after handling source system specific logic or translating transaction system customer ids to standard set of customer id.
* Applies requisite precedence logic to determine most authority source for particular attributes or data sets. Example source image layer may contain multiple sources of customer data. The Source independent data layer provides finalized customer dataset merging information from multiple sources
* Does consolidation and alignment of multiple disparate dataset have similar business meaning
* Not a big-bang approach: Caters to gradual and incremental extension of model
* Use right level of normalization – Has a tolerance of some level of redundancy across the datasets however necessary recon and control should be in place.
* In order to keep the dataset and transformation more manageable, the set of attributes at a given grain shall be broken into multiple tables where required. Example: Customer demographics, customers aggregated transaction profile and aggregated custom service experience attributes can be structured as three datasets
* Maintain historical snapshots of transformed data
* Serves to MIS and needs of data scientist looking for more consolidated and streamlined datasets as their starting point
* Depending on the complexity and usage of the datasets, this layer can be implemented as set of database views, providing agility to implement extensions.
* Depending on whether the composite datasets are deriving generic set of attributes, the same can be made available in public area where users with relevant access are able to leverage
* These datasets should be built in conjunction of SME of business processes owning the data, IT teams from source systems, data architects team and analytics users