---
id: dw_dw_design_and_devlopment_with_use_cases_etl_vs_elt
title:ETL vs ELT
sidebar_label: ETL vs ELT
---


Regardless of ETL or ELT Data transformation/integration process involves the following three steps:

* **Extraction:** Retrieving raw data from an unstructured data pool and migrating it into a temporary, staging data repository
* **Transformation:** Structuring, enriching and converting the raw data to match the target source
* **Loading:** Loading the structured data into a data warehouse to be analyzed and used by business intelligence (BI) tools
![ETL_vs_ELT](/guzzle-docs/img/docs/ETL_vs_ELT.PNG)

### What is ETL?
ETL is an abbreviation of Extract, Transform and Load. In this process, an ETL tool extracts the data from different RDBMS source systems then transforms the data like applying calculations, concatenations, etc. and then load the data into the Data Warehouse system.

In ETL data is flows from the source to the target. In ETL process transformation engine takes care of any data changes.

![etl-processes-described](/guzzle-docs/img/docs/etl-processes-described.png)

Online Analytical Processing (OLAP) data warehouses—whether they are cloud-based or onsite—need to work with relational SQL-based data structures. Therefore, any data you load into your OLAP data warehouse must be transformed into a relational format before the data warehouse can ingest it. As a part of this data transformation process, data mapping may also be necessary to join multiple data sources together based on correlating information (so your business intelligence platform can analyze the information as a single, integrated unit).

That’s why data warehouses require ETL—because the transformations must happens before the loading. Here are some details to understand about ETL:

* **A continuous, ongoing process with a well-defined workflow:** ETL first extracts data from homogeneous or heterogeneous data sources. Next, it deposits the data into a staging area. Then the data is cleansed, enriched, transformed, and stored in the data warehouse.
* **Used to required detailed planning, supervision, and coding by data engineers and developers:** The old-school methods of hand-coding ETL transformations in data warehousing took an enormous amount of time. Even after designing the process, it took time for the data to go through each stage when updating the data warehouse with new information.
* **Modern ETL solutions are easier and faster:** Modern ETL, especially for cloud-based data warehouses and cloud-based SaaS platforms, happens a lot faster. By using a cloud-based ETL solution, users can instantly extract, transform, and load their data from diverse sources without having programming expertise.

### What is ELT?
ELT is a different method of looking at the tool approach to data movement. Instead of transforming the data before it's written, ELT lets the target system to do the transformation. The data first copied to the target and then transformed in place.

ELT usually used with no-Sql databases like Hadoop cluster, data appliance or cloud installation.

![elt-processes-described](/guzzle-docs/img/docs/elt-processes-described.png)


"Data Lakes" are special kinds of data stores that—unlike OLAP data warehouses—accept any kind of structured or unstructured data. Data lakes don't require you to transform your data before loading it. You can immediately load any kind of raw information into a data lake, no matter the format or lack thereof.

Data transformation is still necessary before analyzing the data with a business intelligence platform. However, data cleansing, enrichment, and transformation occur after loading the data into the data lake. Here are some details to understand about ELT and data lakes:

* **A new technology made possible by high-speed, cloud-based servers:** ELT is a relatively new technology, made possible because of modern, cloud-based server technologies. Cloud-based data warehouses offer near-endless storage capabilities and scalable processing power. For example, platforms like Amazon Redshift and Google BigQuery make ELT pipelines possible because of their incredible processing capabilities.
* **Ingest anything and everything as the data becomes available:** ELT paired with a data lake lets you ingest an ever-expanding pool of raw data immediately, as it becomes available. There's no requirement to transform the data into a special format before saving it in the data lake.
* **Transforms only the data you need:** ELT transforms only the data required for a particular analysis. Although it can slow down the process of analyzing the data, it offers more flexibility—because you can transform the data in different ways on the fly to produce different types of metrics, forecasts and reports. Conversely, with ETL, the entire ETL pipeline—and the structure of the data in the OLAP warehouse—may require modification if the previously-decided structure doesn't allow for a new type of analysis.
* **ELT is less-reliable than ETL:** It’s important to note that the tools and systems of ELT are still evolving, so they're not as reliable as ETL paired with an OLAP database. Although it takes more effort to setup, ETL provides more accurate insights when dealing with massive pools of data. Also, ELT developers who know how to use ELT technology are more difficult to find than ETL developers.


### KEY DIFFERENCE
* ETL stands for Extract, Transform and Load while ELT stands for Extract, Load, Transform.
* ETL loads data first into the staging server and then into the target system whereas ELT loads data directly into the target system.
* ETL model is used for on-premises, relational and structured data while ELT is used for scalable cloud structured and unstructured data sources.
* ETL is mainly used for a small or moderate amount of data whereas ELT is used for very large amounts of data.
* ETL doesn’t provide data lake supports while ELT provides data lake support.
* ETL is easy to implement whereas ELT requires niche skills to implement and maintain.


### References:
https://blog.panoply.io/etl-vs-elt-the-difference-is-in-the-how

https://www.xplenty.com/blog/etl-vs-elt/

https://www.guru99.com/etl-vs-elt.html
