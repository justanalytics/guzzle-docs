---
id: dw_dw_design_and_devlopment_use_cases_reporting_cache
title: Reporting Cache
sidebar_label: Reporting Cache
---


Ideally there will be requirement to maintain reporting cache in the SQL server and in some cases on SQL Warehouse.

1. Suggestion is to limit this data to : only required tables, use features of reporting tool to navigate to details when required,
1. Dimension table should be copied fully (except dated ones), fact table should be loaded incrementally.
1. Ensure end to end batch flow covers loading from staging to foundation to aggregate to reporting cache.
1. Ideal to leverage the computation
1. Use appropriate Spark connector for better performance
1. Perform recon to ensure the data ties back
1. Ensure there are no data type alignment issues - including number and date types