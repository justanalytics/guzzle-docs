---
id: arch_arch_and_services
title: Guzzle – Architecture and Services
sidebar_label: Guzzle – Architecture and Services
---

Guzzle is build as combination of Core services and Client services which come together to provide integrated set of accelerators which can achieve [ Guzzle's goal of RACE OIL ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Goals-RACE-OIL)

**Guzzle Core** is made up of,
* Job Definition Store which is basically YML based store for Guzzle job configs.
* Runtime Audit Store which is storing rich set of run-time audit for Guzzle jobs. 
* Set of common services which are built inclusive of orchestration.
* There are 6 internal modules which are to bring data into data lake and to govern, bring resilience and robustness into data integration pipeline. 
   * Batch Ingestion - 
   * Stream Processing - 
   * Data Processing - 
   * CDE Monitoring - to petrol your data before reporting the numbers to users
   * Recon and Trace - to do reconciliation between different layers as ingested data flows through the data lake and traceability to generate data lineage
   * Housekeeping - to provide ability to maintain data life cycle inside data lake through table partitioning

**Guzzle Client** is made up of,
* Web App - allows you author Guzzle jobs by using user friendly Web UI
* Rest API - allows you to work with Guzzle in term of being able to trigger guzzle jobs, job groups or batches through API call
* Guzzle CLI - allows you to work with Guzzle in term of being able to trigger guzzle jobs, job groups or batches through command line

Guzzle does supports wide rage of **sources and targets**. It has very rich set functionalities to work with log files, JDBC sources, APIs, Kafka as a main streaming source, support for adapter like Salesforce and Google Analytics. It also supports different file formats like JSON, XML, Excel, Parquet, ORC, Avro, CSV, delimited files etc.

For **runtime** compute, Guzzle leverages on open source technologies like Spark and Databricks which is powerful in-memory processing.

For **integration** layer, it co-exists with other tools in open source ecosystem. It has native integration with GIT for code versioning, Cucumber for test case automation and Jenkins to run your CI/CD or perform other DevOps activities. It can integrate with Apache Atlas as a set of metadata which you can navigate through to generate lineage. It can use Azure Data Factory and Apache Airflow for job scheduling, but not limited to these tools and Guzzle jobs can be integrated and invoked in other scheduling tools as well.

![Guzzle_Architecture](/guzzle-docs/img/docs/guzzle_architecture_and_services.png)

**Key features** of Guzzle,
1. Native to Spark and Hadoop​

1. Simple to deploy and use​

1. Any to Any data integration : Seamless extensions to new sources and target data stores​

1. Implements commonly used data integration  patterns – enables accelerates build of data pipelines adhering to consistent standards​

1. Handle Diverse workloads : Batch, Micro-Batch, Streaming and API​

1. Enterprise grade Auditability, Governance, Traceability, Provenance and Lineage /metadata​

1. Deeper support for DevOps – has out of box integration with Git (and git workflows), test-automation and auto-deployment​

1. Leverages best of breed open source components​


**For Guzzle Clients**, refer more details [ Guzzle Client ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Client)

**For Guzzle Core services**, refer more details [ Guzzle Core ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Core)