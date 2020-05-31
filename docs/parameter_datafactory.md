---
id: parameter_datafactory
title: Call Guzzle from Azure Data Factory
sidebar_label: Call Guzzle from Azure Data Factory
---

## Create HTTP Linked Service to call Guzzle REST APIs:  
Click on Connections:  
![Screenshot_2020-04-02_at_2.47.03_PM](/guzzle-docs/img/docs/rest_api_connection.png)  


Click on New:  
![Screenshot_2020-04-02_at_2.47.32_PM](/guzzle-docs/img/docs/rest_api_new.png)  


Choose HTTP Linked Service:
![Screenshot_2020-04-02_at_2.47.53_PM](/guzzle-docs/img/docs/rest_api_service.png)


Choose integration runtime. Enter Base URL as Guzzle API URL. If you are using valid SSL certificates (issued by certificate authority) for running Guzzle API then enable Server Certificate Validation. Choose Basic Authentication Type. Enter username and password for native Guzzle user (credentials of Azure AD will not work). Click on Create once it is done.
![Screenshot_2020-04-02_at_2.49.11_PM](/guzzle-docs/img/docs/rest_api_new_service.png)  

## Call Guzzle REST API which triggers Guzzle job:  

Create new dataset:  
![Screenshot_2020-04-02_at_2.50.18_PM](/guzzle-docs/img/docs/trigger_job_new_dataset.png)  


Choose HTTP type of dataset:
![Screenshot_2020-04-02_at_2.50.42_PM](/guzzle-docs/img/docs/trigger_job_http_dataset.png)


Choose format as JSON:
![Screenshot_2020-04-02_at_2.50.57_PM](/guzzle-docs/img/docs/trigger_job_json.png)


Choose Guzzle HTTP Linked Service which was created earlier. Also Specify relative url of Guzzle API
![Screenshot_2020-04-02_at_2.53.20_PM](/guzzle-docs/img/docs/set_property.png)


Add Lookup Activity in ADF Pipeline and configure Settings tab like following:
![Screenshot_2020-04-02_at_2.55.16_PM](/guzzle-docs/img/docs/adf_pipeline.png)
Request body json is like following:
```json
{
  "name": "dq1",
  "jobParameters": {
    "system": "test",
    "business_date": "2020-01-08 18:31:10",
    "guzzle.spark.name": "local1",
    "environment": "test"
  }
}
```

When we debug pipeline, we will get job instance id of triggered job in response of API call:
![Screenshot_2020-04-02_at_3.17.51_PM](/guzzle-docs/img/docs/output.png)


## Call Guzzle REST API which triggers job group:  
Create dataset with relative URL as: **/api/batches/run_job_group**  

Use lookup activity to call API (using HTTP linked service) which triggers job group with following settings:  
**Request Method**: POST  
**Additional Headers**: Content-Type: application/json  
**Request Body**:
```json
{
  "system": "test",
  "location": "SG",
  "business_date": "2020-04-02 16:01:27",
  "guzzle.spark.name": "local1",
  "job_group": "USERS_INGESTION",
  "environment": "test2"
}
```
When we debug pipeline, we will get job instance id of triggered job group in response of API call (similar to job trigger API)  


## Call Guzzle REST API which initializes a batch record:  
Create dataset with relative URL as: **/api/batches/initialize**  

Use lookup activity to call API (using HTTP linked service) which initializes batch record with following settings:  
**Request Method**: POST  
**Additional Headers**: Content-Type: application/json  
**Request Body**:
```json
{
  "contextParams": {
    "system": "sp"
  },
  "businessDate": "2020-04-02 16:11:38",
  "environment": "test2"
}
```
When we debug pipeline, we will not get anything in response of the API call

## Call Guzzle REST API which initializes batch records for multiple days:  
Create dataset with relative URL as: **/api/batches/initialize**  

Use lookup activity to call API (using HTTP linked service) which initializes batch record with following settings:  
**Request Method**: POST  
**Additional Headers**: Content-Type: application/json  
**Request Body**:
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
When we debug pipeline, we will not get anything in response of the API call

## Call Guzzle REST API which triggers a stage of the batch:  
Create dataset with relative URL as: **/api/batches/run_stage**  

Use lookup activity to call API (using HTTP linked service) which triggers stage with following settings:  
**Request Method**: POST  
**Additional Headers**: Content-Type: application/json  
**Request Body**:
```json
{
  "param1": "value1",
  "system": "sp",
  "guzzle.spark.name": "local1",
  "stage": "STG",
  "environment": "test2"
}
```
When we debug pipeline, we will not get anything in response of the API call

## Call Guzzle REST API which triggers multiple stages of the batch:  
Create dataset with relative URL as: **/api/batches/run_stage**  

Use lookup activity to call API (using HTTP linked service) which triggers stage with following settings:  
**Request Method**: POST  
**Additional Headers**: Content-Type: application/json  
**Request Body**:
```json
{
  "param1": "value1",
  "system": "sp",
  "guzzle.spark.name": "local1",
  "stage": "STG,FND,PLP",
  "environment": "test2"
}
```
When we debug pipeline, we will not get anything in response of the API call


