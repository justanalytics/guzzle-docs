---
id: dw_dw_design_and_devlopment_with_use_cases_surrogate_keys
title:Surrogate Keys
sidebar_label: Surrogate Keys
---

Data warehouse surrogate keys are sequentially generated meaningless numbers associated with each and every record in the data warehouse. These surrogate keys are used to join dimension and fact tables.

**In Guzzle processing job, framework generated column `w_sequence_key` can be used to generate surrogate key so it is always unique number.**

> Add more details around how w_sequence_key is generated in Guzzle

In Data Warehouse concept, Surrogate keys cannot be NULLs. Surrogate key are never populated with NULL values.
It does not hold any meaning in data warehouse, often called meaningless numbers. It is just sequentially generated INTEGER number for better lookup and faster joins.

**Why surrogate keys are used in Data warehouse?**

Basically, surrogate key is an artificial key that is used as a substitute for natural key (NK) defined in data warehouse tables. We can use natural key or business keys as a primary key for tables. However, it is not recommended because of following reasons:

1. Natural keys (NK) or Business keys are generally alphanumeric values that is not suitable for index as traversing become slower. For example, prod123, prod231 etc
1. Business keys are often reused after sometime. It will cause the problem as in data warehouse we maintain historic data as well as current data.
For example, product codes can be revised and reused after few years. It will become difficult to differentiate current products and historic products. To avoid such a situation, surrogate keys are used.