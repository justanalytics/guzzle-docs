---
id: guzzle_schedular
title:Guzzle Scheduler
sidebar_label: Guzzle Scheduler
---

User can define multiple schedules in $GUZZLE_HOME/conf/schedules directory

Name of the schedule file will be name of the schedule. e.g. create file "daily_customers.yml" for schedule named "daily_customers"

One schedule config file will look like following:
```yml
version: 1
schedule:
  type: daily/daysofweek/cron
  parallel: true
  properties:
    ...
parameters:
  system: CUSTOMER
  param2: value2
  business_date: ${guzzle.scheduler.systemdate}
  custom_date: ${guzzle.scheduler.systemdate[0..3] + guzzle.scheduler.systemdate[5..6] + guzzle.scheduler.systemdate[8..9]}
runnables:
  - id: 383d9cd8-fc37-4f94-8f32-95cfcc63a62d
    name: job1
    type: job
    environment: dev
    spark_environment: local_spark
    quantity_resource: qr1
    concurrent: false
    parameters:
      location: SG
      param3: ${system}_${location}
    spark_properties:
      ...
  - id: 3fec2f9b-b3a0-4f51-b47b-191ed0e0e091
    name: job_group1
    type: job_group
    environment: test
    spark_environment: hdp_cluster
    quantity_resource: qr2
    parameters:
      location: IN
      param2: new_value2
```


To schedule daily at 01:00,13:00:
```yml
schedule:
  type: daily
  properties:
    trigger_time: 01:00,13:00
```

To schedule at every 2 hours:
```yml
schedule:
  type: daily
  properties:
    trigger_every: 2
```

To schedule at 01:00 every Monday and Thursday:
```yml
schedule:
  type: daysofweek
  properties:
    daysofweek: 1,4
    trigger_time: 01:00
```

To schedule as per custom cron expression at 9:30 am every Monday, Tuesday, Wednesday, Thursday, and Friday:
```yml
schedule:
  type: cron
  properties:
    cron: 0 30 9 ? * MON-FRI
```

$GUZZLE_HOME/conf/schedules/quantity_resource.yml will be config file to define quantity resources:
```yml
version: 1
quantity_resources:
  qr1: 10
  qr2: 5
```

Few implementation notes-  
- Implement scheduler features in guzzle api project  
- We can use spring task scheduler to schedule jobs at some frequency. Check https://www.baeldung.com/spring-task-scheduler for more information  
- If schedule on the job is updated through UI, it should be updated immediately by comparing in memory references of the schedules using id of the runnable item  
- There should be scheduled task that is triggered at regular interval (defined by application.syncSchedule.jobScheduler in application.yml of the api project) that reads schedule files and quantity_resource.yml file and updates in memory references of the schedules using id of the runnable item. There should be api that triggers this schedule immediately (for example check api /api/sync)  
- If value of the qr is increased and if there are waiting runnable items in that qr, those runnable items can start immediately if there is sufficient qr capacity.  
- If value of the qr is decreased, new runnable items will run according to new qr capacity  