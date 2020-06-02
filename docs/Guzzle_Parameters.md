---
id: Guzzle_Parameters
title: Guzzle Parameters
sidebar_label: Guzzle Parameters
---

[[_TOC_]]

## Overview
Guzzle offers wide array of standard parameters and they can be broadly classified into following categories:


## Guzzle System Parameters
This are standard job parameters of Guzzle. They contain contain specific parameters. Some of this are parameters are purely meant for tractability purpose providing the job name, environment, stage, job group etc. Others are meant to control behavior of Guzzle jobs and Guzzle common services. Below table provides full list of this variables and their purpose:

Sr.|Parameter Name| Description | Applicable to |Mandatory|Sample values|References
---|---|---|---|---|---|---
*|job_config_name|This is the name of the job configuration|All job module|Yes (automatically populated)|load_airlines|
*|environment|This contains environment name used triggering the job|All job module| Yes (when running jobs from UI its passed as per the selection on the Top-Right in job list)
*|batch_id|Contains the batch id of the job. A batch usually is used to track the the end to end batch load for a given system|All Job Module|Yes (defaulted to -1 for adhoc job or job group run)|1231321313131|
*|stage_id|This is a stage under which the job was run. Stages are in turn part of batches|All Job Module|Yes (defaulted to -1 for adhoc job or job group run)|1231321313131|
*|job_instance_id|This is the unique job instance id for the individual job run|All job module|Yes|12321313132|
*|business_date|Business date for the job run | All|Yes|2018-01-01 00:00:00|
*|job_group|This is the job group of which this job is part of. Only passed when job is run as part of job group or stage|All job types|No|job_group1
*|stage|Stage name if the job is invoke through a stage run|All Jobs when called from "Run Stage"|N|FND, STG
*|guzzle.spark.name|The spark envrionment name|All|Y|spark_local|
*|guzzle.job_group.partial|Indicates whether a job group allows partial run. When marked as Y will result in running the job 
*|guzzle.ingestion.load_type|This is applicable for ingestion jobs for JDBC. The|Ingestion|N|F: full, I: Incremental|https://gitlab.ja.sg/guzzle/ingestion/issues/31
*|guzzle.batchpipeline.threads|This controls the number of files that are processed in parallel when running a ingestion job. this is applicable when the there are more than one incoming files for  a given job. |Ingestion|No|10|https://gitlab.ja.sg/guzzle/ingestion/issues/114
*|guzzle.stage.resume|This indicates whether a stage has to recover from. This is only applicable when the stage is defined as Partial|Job Groups and Job Stages|N|Y or N|https://gitlab.ja.sg/guzzle/guzzle_common/issues/91
*|hive.storage_format|used as storage format for auto create table|Ingestion|N|



## Context Parameters
When setting up Guzzle environment, one can specify the standard context variables in guzzle.yml which are then available to Stage, Job groups and Job invocation as fixed set of additional parameters. 

<< screenshot to be added latter>>

This context parameters form part of various guzzle runtime audit tables namely: job_info, batch_control, recon_summray, recon_detail, check_constraint_summary,check_contraint_detail,watermark and batch_constraint

Context parameters (also referred as context columns) are designed to bring consistency when tracking common information about data pipelines both in the data table as well as runtime audit and recon tables

Context parameters can also be designed to build sophisticated batch orchestration for large scale data lake implementation ingesting data from multitude of systems, and location. This shall be described in separate document

Context parameters being prompted in the Job, Job group and Run Stage respectively:
<< screenshot to be added latter>>

![image](/guzzle-docs/img/docs/context_parameter.png)

## User  Job Parameters
When creating guzzle job config, one can refer to additional custom parameters. This parameters can then be passed to jobs at the time of invoking. 

The user defined parameters can be passed when invoking the job or via adhoc job_group or when running the Stage (in which case the additional user defined job parameters are passed to all the jobs which form part of the job group or stage


## Precedence Order of Job Parameters
System, context and user parameters can be passed from multiple places. Below is the precedence order in which job parameters are applied when running the job:

### Precedence of user defined and system parameters:

Precedence Order|Layer|Screenshot
---|---|---
1|Parameter passed during Invocation of Run Stage/ Job Group / Job |
2|Environment settings |
3|Parameters specified when adding the Job to Job Group 


### Precedence of Context parameters:

Precedence Order|Layer|Screenshot
---|---|---
1|Parameter passed during Invocation of Run Stage/ Job Group / Job |
2|Parameters specified when adding the Job to Job Group 
3|Environment file |

Note: 1 means highest precedence and 3 means lowest. 


## Using Groovy templates to manipulate Guzzle Parameters
At times the params have to be further modified before it can be used in job definition. Guzzle supports  Groovy templates to allow modifying parameters.

an example of grovvy template below:
csv/user_${business_date[0..3] + business_date[5..6] + business_date[8..9]}.csv

![image](/guzzle-docs/img/docs/groovy_parameter.png)