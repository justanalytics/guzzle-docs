---
id: synapse_reserved_keyword_as_table_name
title: Dealing with Reserved Keywords as a Table Name in SQL Database or Azure Synapse
sidebar_label: Dealing with Reserved Keywords as a Table Name in SQL Database or Azure Synapse
---

There could be instances when you may want to read/write a SQL database or Azure Synapse table which uses a reserved keyword in SQL Server or Synapse SQL Pool as a table name. Guzzle reads/writes table or perform any other compute operations using Databricks in cloud setup or using Apache Spark in on-premise setup.

For example, you want to copy data from Databricks delta to Azure Synapse table and here table name at both ends is used as "user" - which is also a reserved keyword in Azure Synapse. This data copy using Guzzle Ingestion module would fail if Azure Synapse target table mentioned in your Guzzle activity configuration is specified with usual syntax i.e. `<<schema_name>>.user`. Here <<schema_name>> is any of your Azure Synapse target schema name.

This one even fails in SSMS and you need to enclose table name within either square bracket or double quotes in SSMS.

![Synapse-Reserved-Keyword](/guzzle-docs/img/docs/Synapse-Reserved-Keyword.png)

To make this particular scenario work in Guzzle, please use the escape character backslash (\\) in conjunction with double quote (") to enclose your target table name.

e.g. `<<schema_name>>.\"user\"`

This syntax should get you going and copy the Databricks delta table data successfully to Azure Synapse table even if it is also a reserved keyword in Synapse SQL Pool.
