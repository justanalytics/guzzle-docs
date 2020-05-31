---
id: dw_dw_design_and_devlopment_use_cases_use_case_layer
title: Use Case layer
sidebar_label: Use Case layer
---

This layer is meant to create final datasets which are more focused and use case specific

* Contextual dataset for specific use-cases and reporting needs. Data model may undergo constant refactoring for this.
* May keep historical snapshot based on consumption requirement
* Taps on to Source image layer and source independent layer to create requisite use-case specified dataset
* Specific computation, aggregation, derivation and snapshot catering to particular reporting need – example: dataset compliance reporting or input dataset for customer churn model
* Leverages appropriate tools to host the data (graph storage, no-sql (Elasticsearch or HBase), or relational/hive)
* Table names for this layer should follow <<prefix>>_<<entity_name>>. Valid values of prefix are (additional prefix shall be included on case by case basis):
   1. agg: for aggregated
   1. dn: de-normalized tables
   1. snp: snapshot tables
   1. out: outbound tables
* Tables in this layer will have appropriate partitioned schema as per data model requirement. 
