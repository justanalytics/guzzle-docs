---
id: dw_dw_design_and_devlopment_with_use_cases_context_columns
title:Context Columns
sidebar_label: Context Columns
---

Based on your project current and future requirement, you should define the Guzzle context columns in your table.

1. Its recommend to keep context column minimal and depending on their applicability to different data pipelines - as this becomes context param which are prompted for all the jobs and shows most of the report tables
1. Recommend to have prefix for context columns (e.g. "w_") to distinguish them from other data columns example: w_system, w_location.

Few recommended Context columns are listed below. Note that, further additional columns can be added as applicable or any of the below can be removed based on the project specific requirements.

### General Guidance

### Recommended Context column names
| Sr. | Context Column name | Data Type | Purpose | Guzzle parameter/transformation | Partitioned Column | Applicable to which data layer | comments |
|-----|-------------------|---------|---------|---------------------------------|--------------------|--------------------------------|----------|
| 1. | w_business_dt | date/timestamp | This is to capture a data cut date for data consumed from Source System | ${business_date} | Likely | STG, FND, PLP | This date is also used to create data snapshots in Target System if required |
| 2. | w_system | string | This is to capture source system name in Guzzle ingestion job | ${system} | Likely | STG, FND | This context parameter name is editable while setting up the Guzzle in your environment |
| 3. | w_location | string | This is to capture geographic location in Guzzle ingestion job if Source System data is certain location specific | ${location} | Likely | STG, FND | This context parameter name is editable while setting up the Guzzle in your environment |


Follow the wiki page link for few more detail regarding [ Guzzle Parameters ](Guzzle-Parameters.md)