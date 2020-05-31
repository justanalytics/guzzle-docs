---
id: dw_dw_design_and_devlopment_with_use_cases_file_extracts
title:File Extracts
sidebar_label: File Extracts
---


Whenever data is consumed from delimited files, format standardization should be done to make extracted files or manual files easy to consume and to avoid few common issues while consuming data from delimited files.
1.	Use carat (^) as column delimiter – it is one of the character very unlikely to be used in free text application fields
1.	Use double quote (“ “) as text qualifier
1.	Extract all date columns in YYYY-MM-DD format and timestamp columns in YYYY-MM-DD HH:MI:SS format. This is default date format followed by most databases including hive and Databricks delta tables.
1.	It is always recommended to include column headers in source file without spaces or any special characters in column names,\
i.	Guzzle can auto map columns from source file to stage target table if column names are matching between source and target. No explicit mapping required\
ii.	It is easy to debug when developer need to backtrack data to the file in case there are any data issues identified in target
1.	Character encoding UTF-8 is recommended as it works well while reading files in Windows as well as Linux hosts
1.	Generate control file in Guzzle supported format – control file should have exact same name as of corresponding data file with different extension. For example, data file ABC_20200319.dat should have corresponding control file ABC_20200319.ctl\
i.	Control file should always have 2 columns i.e. count, checksum - here count should be record count excluding header record count (if any) and checksum column can be left null as it is not yet supported in Guzzle and feature could be made available in future releases. Control file shall always be comma (,) separated as expected by Guzzle.
Example:  
Header  count,checksum
Data       9800,\
ii.	Control file validation helps to identify if file is truncated or corrupted during network file transfer between one host to another host (if any)
1.	It is recommended to include date in file name YYYYMMDD[_HHMISS] - it should indicate as of data cut date in case of full extract files and delta extraction date in case of incremental file
1.	Data file should use “.dat” extension and control file (if any) should use “.ctl” extension
1.	Numeric columns should not contain thousand separator (,) in extracted file. If column is defined with numeric datatypes (smallint, tinyint, bigint, float, decimal etc.) in target database table then numeric data containing thousand separator in source file is considered as string and value will be populated null in target table.
