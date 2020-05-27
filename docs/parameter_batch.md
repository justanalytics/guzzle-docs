---
id: parameter_batch
title: Guzzle Batch (formerly Contexts)
sidebar_label: Guzzle Batch (formerly Contexts)
---


## Guzzle Batch (formerly known as Contexts)

Guzzle Batch is a comprehensive approach to handle diverse workloads like Batch, Micro-Batch, Streaming and API.
- A batch can be defined in a context of loading a particular system data or a particular geographic location data or even a combination of multiple context columns.
- A batch can be initialized to execute for a given single business date
- A batch can be initialized to execute for the range of business dates by passing start date, end date and period runtime parameters. To read more about batch initialization options, go through wiki-page [ Guzzle Client ](https://gitlab.ja.sg/guzzle/docs/-/wikis/Guzzle-Client)
- A batch can be configured to allow or not to allow re-execution using option `Rerun Batch`
- A batch can be configured for `Stage Pair`, if a batch has more than one stage defined. Stage pairing is very interesting concept and configured as appropriate to your workload whenever batch is executed in catch-up mode to run for multiple days. For example, lets assume you have a Batch-1 which has 3 stages defined into it namely - Stage-1, Stage-2 and Stage-3. If Batch-1 has not executed for last 2 days due to some planned system maintenance or some unplanned issues then on Day-3, Batch-1 can either be initialized and executed for latest business date or can be initialized and executed for last 3 day's business dates - it is depending on your batch initialization config. Here on Day-3, if Batch-1 is initialized to run for last 3 days in catch-up mode then in absence of stage pairing, it will clear Stage-1 jobs first for all 3 business dates, next it will clear Stage-2 jobs for all 3 business dates and finally it will clear Stage-3 jobs for all 3 business dates. But if you define stage pairing for Stage-1, Stage-2 and Stage-3 then it will clear all Stage-1, Stage-2 and Stage-3 jobs first for (day - 2) business date (oldest), next it will clear all Stage-1, Stage-2 and Stage-3 jobs for (day - 1) business date and finally it will clear all Stage-1, Stage-2 and Stage-3 jobs for (day - 0) business date. It is important you understand to appreciate this feature and use it as appropriate to define batches for your workload requirements.
- A batch stage can contain one or more pipelines (formerly know as Job Groups) and each stage can be configured to allow reruns using `Rerun Batch` option.
- A batch stage can also be configured to `Partial Load` to allow batch execution to continue further even if any jobs within pipelines called in the batch stage fails. Please note if `Partial Load` is not enabled then batch execution stops right there as soon as there is any job failure occurs within pipelines called in the batch stage.
- A batch stage also has option called `Validate SQL` which is used to write any SQL validation query which in turn, if evaluates to `TRUE` then batch execution continues to execute that particular batch stage and if it evaluates to `FALSE` then batch execution stops right there without executing that particular batch stage. This is most often used to handle upstream dependencies where you may want to check first if any upstream batch is completed successfully or not before proceeding with current batch stage load. Such upstream Guzzle batch status can always be queried using Guzzle runtime audit table `batch_control` or even by querying a table `job_info` for checking upstream individual job level statuses.

A batch can be defined as collection of one or more stages to load data into the data lake. Below is visual illustration of a Guzzle batch and its control workflow,

## Guzzle Batch Control Flow

![Guzzle_Batch_Control_Flow](/guzzle-docs/img/docs/Guzzle_Batch_Control_Flow.png)

As discussed above Guzzle batch is quite a deep concept and batch can be configured to handle various workload types. As illustrated above in the control flow diagram,

- Guzzle **batch** comprise one or more stages. All stages run in sequence. Stage sequence you can define while defining your Guzzle batch. Batch can be configured 
- A **stage** can contain one or more pipelines. Each stage can map to ELT/ETL paradigm we typically use to ingest and process source data in a layered manner to build data warehouse. For example, data staging layer, reusable layer, use-case layer etc. Depending upon project use-case, we can define and abbreviate stages to be configured during Guzzle initial setup as follows,
   * Staging or Source Image layer - `STG`
   * Foundation or Reusable layer - `FND`
   * Post Load Processing or Use-Case Layer - `PLP`
   * Snapshot layer - `SNP`
   * Extraction or External layer - `EXT`
- A **pipeline** (formerly known as Job Group) is logical grouping of one or more activities.
- An **activity** (formerly known as Job Configs) is the one where you implement your business rules. It contains actual task definitions which could be of type ingestion, processing, housekeeping, external etc.