---
id: goal_race_oil
title: Guzzle Goals RACE OIL
---


Key goals of Guzzle is to build frameworks that are:

1. **Robust**: Caters to resilience and robustness of building and deploying in data integration solutions. Fail-over and recovery, tight handling of control variables, exceptions, tracebility. Cater go straight through process, It should use cluster , support multiple parallel pipeline

2. **Accelerate**: The whole purpose of building this frameworks is to accelerate the implementation of analytics marts and data lake projects. The framework should capture  all the repetitive patterns which are required for typical data integration project and provide reasonable level abstractions and configurations(not too low level like traditional ETL tools).

3. **Consistency**: The frameworks should bring the consistency and predictability in a deployment. Consistency also implies no redundancy. All the key  patterns around data  ingestion, transformation, logging and loading patterns should be be centralized. 

4. **Extensible**: Fully extensible in terms of sources and target supported, stages of data flow, instrumentation/logging and reporting, metadata, context of data integration 

 

Other goals:

1. **Open source**: To build on top of existing open source projects as much possible

2. **Integrated yet Modular**: While each components are very well integrated and complement each other -it should support devt, enhancement and deployment of each of the module independently. 

3. **Lightweight** : The framework should be lightweight in terms of runtime overhead  and effort to deploy, configure and have it up and running.****************