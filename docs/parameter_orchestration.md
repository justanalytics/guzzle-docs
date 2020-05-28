---
id: parameter_orchestration
title: Orchestration of ADF pipeline with Guzzle and Non Guzzle Jobs
sidebar_label: Orchestration of ADF pipeline with Guzzle and Non Guzzle Jobs
---


[[_TOC_]]

# Overview

In Azure cloud, there are wide range of features available for Compute, Storage, ELT/ETL Orchestration, Databricks Notebooks, Stream Analytics, ML/AI capabilities and many of them are supported by Guzzle for integration while I am writing this wiki page, and support for few of them is currently work in progress. Hence while orchestrating end-to-end ELT/ETL data flow pipeline - starting from data consumption from ultimate application data sources to the final reports/dashboards generation for the end user consumption may involve various Guzzle as well as Non-Guzzle components. So the question is - how do we possibly orchestrate this by leveraging on best of the features available in Guzzle and Azure Data Factory to build the end-to-end data pipeline in Azure cloud setup?

After multiple considerations to answer that question, we decided to use Azure Data Factory (ADF) to orchestrate end-to-end data pipeline if you are using Guzzle on Azure cloud setup. ADF can integrate well and can execute mixed set of job types by calling corresponding technology specific APIs which includes - executing Guzzle batches, Databricks Notebooks, Azure Logic Apps, Azure Native Pipelines, Shell Scripts, Powershell Scripts etc. It should be noted that, Guzzle also has road-map to support integration with most of these Non-Guzzle components using Guzzle External job type in near future. This is already work in progress and feature will be available soon.

Azure Date Factory supports event based and time based job execution which is at par feature to use it as a scheduler in Azure cloud platform, though it doesn't have built-in support for defining inter-dependencies across the ADF native pipelines and concept of order date snapshots supported by most specialized scheduling tools to execute all the jobs/pipelines for a specific order date.

Below are few important concepts and considerations to keep in mind while orchestrating ADF + Guzzle end-to-end pipeline.

# Important Concepts and Considerations

## Guzzle batch and its control flow

![Guzzle_Batch_Control_Flow](/guzzle-docs/img/docs/Guzzle_Batch_Control_Flow.png)

Guzzle batch is a deep concept and below is just a brief description for component you can see in above Guzzle batch control flow diagram,
* Guzzle **batch** comprise one or more stages. All stages run in sequence. Stage sequence you can define while defining your Guzzle batch.
* A **stage** can contain one or more pipelines. Each stage can map to ELT/ETL paradigm we typically use to ingest and process source data in a layered manner to build data warehouse. For example, data staging layer, reusable layer, use-case layer etc.
* A **pipeline** is logical grouping of one or more activities.
* An **activity** is the one where you implement your business rules. It contains actual task definitions which could be of type ingestion, processing, housekeeping, external etc.

For more details, please refer wiki-page [ Guzzle Batch ](parameter_batch.md)

## Invoke Guzzle batch from ADF using Guzzle API

Now once you develop the Guzzle batches - how do you trigger it from ADF by making a call to Guzzle API? What are the configuration steps to be followed? To answer those questions, there is a separate wiki page to cover this topic in details. Hence please refer 
[ Call Guzzle from Azure Data Factory ](parameter_datafactory.md)

## Guzzle API Base URL to configure in ADF HTTP linked service

You can locate Guzzle API base URL to be configured in ADF HTTP linked service from *guzzle.yml* file from your Guzzle host.
This file is available under directory *$GUZZLE_HOME/conf/*

![Base_API_URL](/guzzle-docs/img/docs/Base_API_URL.png)

## Single day and explicit multiple day Guzzle batch initialization

* **Single day batch initialization** creates a Guzzle batch in `batch_control` table only for the given business date during Guzzle API call. For example,

**Init Batch Request Body**:
```json
{
  "contextParams": {
    "system": "sp"
    "location": "all"
  },
  "businessDate": "2020-04-02 16:11:38",
  "environment": "test2"
}
```

This is mostly used for batches where data is full load and there is no specific requirement to maintain the continuous business date snapshots into the target tables. It can also be used for batches where source data is incremental in nature and target is append or merge with no snapshots maintained, and as long as source can provide collective incremental file for the days when batch loads were missed out due to system outages or planned downtime for maintenance.

* **Multiple day batch initialization** creates the Guzzle batches in `batch_control` table for explicit range of start date, end date and period provided during Guzzle API call. For example,

**Init Batch Request Body**:
```json
{
  "contextParams": {
    "system": "sp",
    "location": "all"
  },
  "businessDateRange": {
    "startDate": "2020-04-02 16:00:00",
    "endDate": "2020-04-06 16:00:00"
  },
  "period": "1",
  "environment": "test2"
}
```

This is mostly used for batches where data is full or even incremental in nature and there is requirement to maintain the continuous business date snapshots into the target tables. In this case, if batch loads are missed out due to system outages or planned downtime for maintenance then once system is up, Guzzle should catch-up by executing batch load for missed range of dates and generate respective business date snapshots into target.

## Non-guzzle components in the middle of end-to-end batch processing

There could be scenarios where your end-to-end batch processing has Non-Guzzle components in the middle like in below data flow example,

**Step 1:** Load data from Source to staging layer using Guzzle jobs \
**Step 2:** Load data from staging to reusable layer using ADF native pipeline\
**Step 3:** Load data from reusable to use-case layer using Guzzle jobs\
**Step 4:** Copy data from use-case layer to reporting cache (if any) using Guzzle jobs

In above example, since middle Step 2 is Non-Guzzle component then you will have to split the Guzzle batch possibly into two batches, 1st Guzzle batch for Step 1 and 2nd Guzzle batch for Step 3 and Step 4 combined. Here Step 2 is taken care by ADF native pipeline and this could be because of some client specific requirements. If you orchestrate and schedule the master pipeline in ADF for this end-to-end data load, first you will have Guzzle API call to 1st Guzzle batch to perform Step 1, then you will have the ADF execute pipeline activity to run ADF native pipeline for performing Step 2 and finally you will have another Guzzle API call to 2nd Guzzle batch to perform Step 3 and Step 4 to finish all data loading steps.

Here note that, if Step 2 would have also been implemented using Guzzle jobs then you can possibly orchestrate this end-to-end data load using single Guzzle batch and just schedule that single batch within ADF master pipeline by giving a Guzzle API call.

## Non-guzzle components at the start or at the end of end-to-end batch processing

There could be scenarios where your end-to-end batch processing has Non-Guzzle components at the start or at the end like in below data flow example,

**Step 1:** Load data from Source to staging layer using ADF native pipeline \
**Step 2:** Load data from staging to reusable layer using Guzzle jobs\
**Step 3:** Load data from reusable to use-case layer using Guzzle jobs\
**Step 4:** Copy data from use-case layer to reporting cache (if any) using Guzzle jobs

In above example, since Step 1 is Non-Guzzle component then you may perform other steps (excluding Step 1) using single Guzzle batch. This can be done by combining Step 2, Step 3 and Step 4 as stages in a Guzzle batch. If you orchestrate and schedule the master pipeline in ADF for this end-to-end data load, first you will have an ADF activity to execute ADF native pipeline to perform Step 1 and second activity will have Guzzle API call to Guzzle batch to perform Step 2, Step 3 and Step 4 to finish rest of data loading steps.

## Using configuration table to pass parameter values to dynamically construct JSON format for Guzzle API call

Below is a sample for configuration table you may create to build generic ADF pipeline to call Guzzle API for executing all your batches. You can build, populate and lookup such a configuration table within your ADF pipeline to construct Guzzle API JSON format dynamically and pass this constructed dynamic JSON contents to an API call which can execute any of your Guzzle batches.

| ID | Batch_Name | Batch_Context_Params | Run_Stage | Batch_Additional_Params | Spark_Environment | Is_Multi_Day_Call | Blob_SAS_URL | Blob_SAS_Token |
|----------|----------- |----------------------|-----------|-------------------------|-------------------|-------------------|--------------|--------------|
| 1 | SRC2FND_system1 | "system": "SRC2FND_system1","location": "All" | STG,FND | "environment": "env_uat" | guzzle-data-engineering | N | https://storacctdiuat.blob.core.windows.net/xxxxxxx | ?xxxxxxx |
| 2 | FND2PLP_system1 | "system": "FND2PLP_system1","location": "All" | PLP | "environment": "env_uat" | guzzle-data-engineering | N | https://storacctdiuat.blob.core.windows.net/xxxxxxx | ?xxxxxxx |
| 3 | DB2SYNAPSE_system1 | "system": "DB2SYNAPSE_system1","location": "All" | PLP | "environment": "env_uat" | guzzle-data-engineering | N | https://storacctdiuat.blob.core.windows.net/xxxxxxx | ?xxxxxxx |
| 4 | SRC2PLP_system2 | "system": "SRC2PLP_system2","location": "All" | STG,FND,PLP | "environment": "env_uat","period": "1" | guzzle-data-engineering | Y | https://storacctdiuat.blob.core.windows.net/xxxxxxx | ?xxxxxxx |

* **ID:** This is just unique sequence number (static) used in configuration table. It can be used as a filter in your lookup activity which would query this configuration table.
* **Batch_Name:** This is a descriptive name given to each of the batch. This column is insignificant for Guzzle API call. It can also be used for logically grouping multiple batches into one to showcase end to end data load for a particular system or for a business segment or for department. Such logical grouping of batches can also be useful for creating runtime audit dashboards.
* **Batch_Context_Params:** These are batch context parameters to be passed to Guzzle API call. It is comma separated key-value pair.
* **Run_Stage:** These are batch stages to be passed to Guzzle API call for their execution. It is comma separated values.
* **Batch_Additional_Params:** These are additional parameters you may want to pass to Guzzle API call. It is comma separated key-value pair.
* **Spark_Environment:** This is Spark cluster to be passed to Guzzle API call which you might have configured in Guzzle UI under Environment section.
* **Is_Multi_Day_Call:** This is flag maintained to decide weather to construct single day or multiple day init batch JSON syntax for executing given batch.
* **Blob_SAS_URL:** This is blob container SAS URL which hosts Guzzle logs in your environment. It can be used to send Guzzle log location in post load email notification.
* **Blog_SAS_Token:** This is blob container SAS token in your environment. It can be used to send Guzzle log location in post load email notification.

Apart from these set of columns, you may add and maintain other additional column suitable to your project requirements within configuration table. This sample is just to give you fair understanding on - how to maintain configuration in table for constructing Guzzle API call dynamically to build generic pipeline.

## Context columns and control columns to be maintained in tables

You should always maintain some standard set of context column (as applicable) and control columns in tables across staging layer, reusable layer and use-case specific layer which are very helpful for table partitioning or for troubleshooting at times.

```sql
    `w_src_file_name`     string,
    `w_refresh_ts`        timestamp,
    `w_job_instance_id`   bigint,
    `w_batch_id`          bigint,
    `w_business_dt`       date,
    `w_system`            string,
    `w_location`          string
```

* For more details refer wiki page [ context columns ](context_column.md)
* For more details refer wiki page [ audit/control columns ](audit_column.md)

## Time based vs Event based scheduling

Once pipeline is developed, you may want to schedule it at daily/weekly/monthly frequency for execution.

You can schedule it either for event based trigger or time based trigger,

**Time based trigger in ADF**
* Time based trigger can be configured in ADF by adding a trigger to your pipeline where you can define fixed execution schedule. For example, run daily at 08:00PM or run every Monday at 07:00AM etc.
* Time based trigger can also be configured in ADF by adding tumbling window trigger for pipeline execution.
![Time_based_trigger](/guzzle-docs/img/docs/Time_based_trigger.png)

**Event based trigger in ADF**
* Event based trigger can be done based on success or on failure or on completed or on skipped status of the previous activity within the pipeline.
![Event_based_trigger](/guzzle-docs/img/docs/Event_based_trigger.png)
* Event based trigger can also be implemented by adding a file watcher event. It can also be achieved using Get Metadata activity within ADF pipeline.
![Event_based_trigger_2](/guzzle-docs/img/docs/Event_based_trigger_2.png)

**Hybrid trigger mechanism**
* As there could be scenarios where you may need to add dependencies across pipelines running at different time. Such across the pipeline event based trigger can achieved using below steps, 
   * Use time based execution for your pipeline which will implement until activity to check status of upstream batches or pipelines
   * Use combination of wait and lookup activity within until loop to query `batch_control` table or ADF runtime audit table to check if corresponding upstream batches or pipelines are already successful.
![Hybrid_trigger](/guzzle-docs/img/docs/Hybrid_trigger.png)

### Challenges in pipeline/batch design while consuming data from multiple time based sources
If there are multiple time based sources to be ingested into your staging layer and your subsequent layer loads has to wait until data from all the sources is available in staging then you should consider splitting your pipeline/batch to ingest data from each of your source system at specific time and you should implement hybrid mechanism as described above for executing your subsequent pipeline/batch to achieve continuous execution of your end to end data load without having to leave any buffer time in-between the upstream and the downstream pipeline/batch to trigger your downstream loads.

For example:
1. Source system A is available and ingested to staging layer daily at 07:00 PM
1. Source system B is available and ingested to staging layer daily at 08:30 PM
1. Source system C is available and ingested to staging layer daily at 09:00 PM
1. Assuming all sources finishes ingestion to staging at 09:15 PM under optimal execution circumstances, your staging to subsequent layer loads can start daily immediately at 09:15 PM without leaving any buffer time in-between, if you implement the looping mechanism described above for hybrid trigger. 

This eventually reduces overall batch execution time for your end to end data load.

---
# Real Life Project Use Case
Now lets go through the real life project use case where we used ADF + Guzzle to orchestrate the end to end pipeline which performs following activities,
* Extract the data files from application source to blob storage using ADF pipeline
* Load extracted data files from blob storage to Databricks delta stage tables using Guzzle context
* Process data from stage to reusable layer using Guzzle context
* Process data from reusable to use-case layer using Guzzle context
* Perform ML using Databricks PySpark notebook
* Copy data from Databricks delta tables to Azure Synapse using Guzzle context
* Send email notification in case of failures

![ADF_Sample_Use_Case_Master_Pipeline](/guzzle-docs/img/docs/ADF_Sample_Use_Case_Master_Pipeline.png)

## Extract the data files from application source to blob storage using ADF pipeline
* If you need to extract data files from application source before you could consume that data then it is recommended to extract data into Parquet file format as it enforces the data types on extracted data. This format is also recommended by Databricks as it is optimized and highly tuned to perform really well for Bigdata systems. As Parquet files uses binary formats for storing tables, the overhead is less than required to parse a CSV file. Parquet is the big data analogue to CSV as it is optimized, distributed, and more fault tolerant than CSV files.
* Include extraction date and time as part of extracted file name (refer \# 1 in above ADF pipeline screen capture). Business date can be used to include as part of file name suffix.
* ADF can be configured to extract data into parquet file format (refer \# 2 in above ADF pipeline screen capture) and Guzzle also supports Parquet format for ingestion job type.
* Major advantage of extracting data into parquet format is - it can enforce schema on the extracted data which is big plus to avoid common issues while consuming data from delimited text files. There are other formats also to enforce data type like ORC, Avro etc.
* If you have very specific requirement to extract data into delimited text files or have to consume data from manual files then you should consider enforcing few standards beforehand, so that, extracted delimited files or manual files can be standardized for downstream consumption to avoid certain issues.
* Refer the wiki page for recommended practices while consuming [ delimited or manual file extract ](file_extraction.md).

## Load extracted data files from blob storage to Databricks delta staging layer tables using Guzzle context

* Once data is ready for consumption from extracted files, Guzzle batch can ingest it into staging layer (refer \# 3 in above ADF pipeline screen capture).
* Here stage STG is defined under a Guzzle batch to ingest data into staging layer maintained as Databricks delta tables.

   **Note:** In few scenarios data might directly be consumed from application source systems also instead of consuming it from the extracted files.

## Process data from staging layer to reusable layer using Guzzle context

* As data is ingested from files to staging layer, Guzzle batch can process it further and load into reusable layer (refer \# 3 in above ADF pipeline screen capture).
* Here stage FND (referred as ODS in screen capture) is defined under a Guzzle batch to process and load data into reusable layer maintained as Databricks delta tables.

   **Note:** Layer specific abbreviated notations may differ project to project and you may use what's defined in your project.

## Process data from reusable layer to use-case layer using Guzzle context

* Once data is loaded into reusable layer, a separate Guzzle batch can process it or aggregate it further to load into use-case specific layer (refer \# 4 in above ADF pipeline screen capture).
* Here stage PLP (referred as ABT in screen capture) is defined under a Guzzle batch to process and load data into use-case layer maintained as Databricks delta tables.

   **Note:** Layer specific abbreviated notations may differ project to project and you may use what's defined in your project.

## Perform ML using Databricks PySpark notebook

* Use-case layer data is used by PySpark notebook which uses Pandas libraries to perform ML and derive some projections (refer \# 5.2 in above ADF pipeline screen capture).
* This is again Non-Guzzle component in end to end data flow and thus Databricks Notebook is directly invoked in ADF pipeline using Notebook activity. Notebook path and other runtime details can also be configured in configuration table we discussed earlier. These runtime details can be fetched using lookup activity and passed to Notebook activity as seen in \# 5.1

## Copy data from Databricks delta tables to Azure Synapse using Guzzle context

* There is another Guzzle batch defined to copy data from Databricks delta tables to Azure Synapse Analytics.
* Azure Synapse Analytics is acting as a reporting cache which is eventually queried by Power BI to generate reports and dashboards.

## Configure and send email notification for batch execution

You can configure email notification table as below to populate email IDs of specific team within your project or specific departments in your organisation.

| ID | Team | Email |
|----|------|-------|
| 1 | Data Engineer | john@ja.com; naveen@ja.com; tin@ja.com |
| 2 | Data Science | kelvin@ja.com; kanika@ja.com |
| 3 | Data Analyst | umesh@ja.com |
| 4 | Operations | bhavana@ja.com; fredo@ja.com |

This table can be used to lookup based on ID filter to get email ids. Email ids can be passed to web activity which calls Logic App URL to trigger email notification either on pipeline success or on failure. 
![Email_Notification_Web_Activity](/guzzle-docs/img/docs/Email_Notification_Web_Activity.png)

You can include below sample details in email alert by using built-in ADF parameters and by querying Guzzle runtime audit tables like `batch_control`, `job_info` and `job_info_param`.

**Sample SQL to query Guzzle runtime audit tables**
```sql
select job_info.*,
(select parameter_value from dbo.job_info_param where 1=1 and parameter_name = 'job_status_url' and job_info_param.job_instance_id = job_info.job_instance_id) databricks_log_url,
(select concat('<<blob container URL>>',parameter_value,'<<blob query string>>') from dbo.job_info_param where 1=1 and parameter_name = 'log_file' and job_info_param.job_instance_id = job_info.job_instance_id) guzzle_log_url
from dbo.job_info
where 1=1
and job_info.batch_id='<<current batch id>>'
and job_info.status in ('FAILED','ABORTED') and job_info.tag not in ('workunit', 'publish')
order by job_info.job_instance_id desc
```

**Sample email alert contents**
![Email_Notification](/guzzle-docs/img/docs/Email_Notification.png)

## Generic ADF pipelines template for Guzzle API call
1. Generic pipeline to dynamically construct JSON using configuration table for Guzzle API call
![ADF_Guzzle_Construct_API_JSON_Pipeline](/guzzle-docs/img/docs/ADF_Guzzle_Construct_API_JSON_Pipeline.png)
   **Note:** Sample for configuration table we have discussed earlier

1. Generic pipeline for Guzzle API call for - init batch and run stage
![ADF_Guzzle_API_Call_Pipeline](/guzzle-docs/img/docs/ADF_Guzzle_API_Call_Pipeline.png)

1. Generic pipeline to wait for running batch to finish\
 ![ADF_Guzzle_Track_Batch_Pipeline](/guzzle-docs/img/docs/ADF_Guzzle_Track_Batch_Pipeline.png)

1. Generic pipeline to wait for running batch stage to finish

 ```sql
 select <<STG/FND/PLP>>_status from dbo.batch_control where batch_id=<<current batch id>>
 ```
![ADF_Guzzle_Track_Batch_Stage_Pipeline](/guzzle-docs/img/docs/ADF_Guzzle_Track_Batch_Stage_Pipeline.png)

5. Generic ADF pipeline exported template (refer attachment)
   * To import in ADF, **click plus (+)** sign to Add new resource
   * Choose **Pipeline from template**
   * Select **Use local template**
   * Select zip file of downloaded template from your local machine and click open to upload
   * Configure database linked service prompts for your environment
   * Configure HTTP server linked service prompts for your environment
   * Click **Use this template**
   * All pipeline components would be imported into your ADF environment, click **Publish all** to save changes

  Refer attached for exported template [PrepareRequestBodyAndInvokeGuzzleBatch.zip](/guzzle-docs/img/docs/PrepareRequestBodyAndInvokeGuzzleBatch.zip)
