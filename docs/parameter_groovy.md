---
id: parameter_groovy
title: Groovy expression to manipulate Guzzle Parameters
sidebar_label: Groovy expression to manipulate Guzzle Parameters
---


## Using Groovy templates to manipulate Guzzle Parameters

You can use Groovy expression to manipulate Guzzle parameters. One of typical use case is altering date formats to the system specific date format. At times the params have to be further modified before it can be used in job definition. Guzzle supports Groovy templates to allow modifying parameters.

Example of groovy template below: 

Lets say files to be consumed are received under "csv" directory with date embedded in file name.

**user_20200429.csv**

The Guzzle Ingestion job source file pattern to read this file would be,

**csv/user_${business_date\[0..3\] + business_date\[5..6\] + business_date\[8..9\]}.csv**

![image](/guzzle-docs/img/docs/parameter_groovy_expression.png)