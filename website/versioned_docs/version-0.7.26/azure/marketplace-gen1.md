---
id: version-0.7.26-marketplace
title: Guzzle on Azure Marketplace
sidebar_label: Installing on Azure Marketplace
original_id: marketplace
---


## Overview
1. Guzzle is available on Azure Marketplace at https://azuremarketplace.microsoft.com/en-us/marketplace/apps/justanalytics.guzzle-databricks?tab=Overview

## Network Architecture for Guzzle on Azure
![image](/guzzle-docs/img/docs/guzzle_network_architecture.png)

## Pre-requisites 
Ensure you have following resource
The list is also captured at: https://gitlab.ja.sg/guzzle/docs/-/wikis/Design/Azure-Marketplace-Offering-Gen-1#solution-template

1. Empty Resource group created in one of your existing subscription. This subscription is treated as primary subscription 
1. Managed identity created in the Tenant (Azure Active Directory)
1. Storage account and container  - This has to be blob storage (and not ADLS/Hierarchy namespace). Also the Managed Identity in step 2 should have full owner permission to this storage account (not just the container). Also the blobstorage is open to 
![image](/guzzle-docs/img/docs/guzzle_marketplace_pre_req.png)
1. SQL Server database to host Guzzle repository. Only native/local accounts are supported  (Azure AD accounts are not supported)
1. Separate SQL Server database to host databricks metastore . Only native/local accounts are supported  (Azure AD accounts are not supported). 
1. Both SQL server databases can be in same of different server 
1. Databricks workspace name, region, organization id and  Access token 
1. Service Principle /Application registration to support single sing-on : https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app (this involves step in Azure AD to update the redirect URL)
**Note: ** If you don't have the "Service Principle /Application registration", just put any xxx (or some arbitrary string) for clientid and client secrete. You can always update this latter with correct value for SSO to work

## Must to know
1. Don't have special character in the passwords - specially $ and | 
2. Ensure Azure SQL server Database is firewall rules allows all Azure resources to connect to it (Azure SQL Server connections shall happen from Databricks and Guzzle VM)
![image](/guzzle-docs/img/docs/azure/must_know.png)
3. Guzzle Storage Account and Guzzle VM should be in same subscription (the setup script takes the VM's subscription and uses that to mount blob storage)
4. Password for External metastore for databricks is stored as plain text in Guzzle configs. its recommended to switch to internal metastore once Guzzle marketplace offer is up and running


## Deployment Steps

### Basic Info
![image](/guzzle-docs/img/docs/azure/offer_wizard_1.png)

### VM Details and Managed Identity
![image](/guzzle-docs/img/docs/azure/offer_wizard_2.png)

### Guzzle Settings
![image](/guzzle-docs/img/docs/azure/offer_wizard_3.png)

### Databricks Settings
![image](/guzzle-docs/img/docs/azure/offer_wizard_4.png)

### Review and Create
![image](/guzzle-docs/img/docs/azure/offer_wizard_5.png)

### Upon completion of Deployment
![image](/guzzle-docs/img/docs/azure/offer_wizard_6.png)


## What will you see when its deploying Marketplace offer

### In Guzzle VM
1. The deployment is progressing. The setup script can take upto 10 minutes as it copies 500MB+ of files over to blob store
2. You see the setup script for python  running
![image](/guzzle-docs/img/docs/azure/running_processes.png)
1. All the logs goes in this folder: /var/lib/waagent/custom-script/download/0/ in VM. stderr and stdout has all the key information
```shell
demoadmin@guzzlemp2vm:~$ sudo bash
root@guzzlemp2vm:~# cd /var/lib/waagent/custom-script/download/0/
root@guzzlemp2vm:/var/lib/waagent/custom-script/download/0# ls -ltrh
total 28K
drwxr-xr-x 2 root root 4.0K Apr 10 07:41 scripts
drwxr-xr-x 2 root root 4.0K Apr 10 07:42 logs
-rw------- 1 root root 3.7K Apr 10 07:42 stderr
-rw------- 1 root root  16K Apr 10 07:46 stdout
root@guzzlemp2vm:/var/lib/waagent/custom-script/download/0# date
Fri Apr 10 07:51:56 UTC 2020
root@guzzlemp2vm:/var/lib/waagent/custom-script/download/0#
```
1. Finally once setup is complete you should see following processes running in Guzzle VM ( There are the ones which may be missing and can be ignored : sudo --preserve-env=PATH -HEu demoadmin )
  1. bloufuse to mount Guzzle home blobg container to VM
  2. Elastic search used by Atlas
  3. Node server (web server of Guzzle)
  4. Elastic search by Guzzle
  5. Atlas Java process
  6. Guzzle API process


```shell
oot@guzzlemp2vm:/guzzle/logs# ps -ef | grep "[g]uzzle\|[n]ode\|[e]lastic\|[a]tlas"
root       1323      1  1 04:10 ?        00:03:20 blobfuse /guzzle --tmp-path=/mnt/blobfusetmp -o allow_other --config-file=/root/fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 --file-cache-timeout-in-seconds=10
root       1326      1  0 04:10 ?        00:00:00 sudo --preserve-env=PATH -HEu demoadmin bash -c /opt/elasticsearch-6.2.4/bin/elasticsearch
root       1473      1  0 04:10 ?        00:00:00 sudo --preserve-env=PATH -HEu demoadmin bash -c java -Dloader.path=/guzzle/api/libs -jar api-0.0.1-SNAPSHOT.jar
demoadm+   1478   1473  0 04:10 ?        00:02:02 java -Dloader.path=/guzzle/api/libs -jar api-0.0.1-SNAPSHOT.jar
demoadm+   1543   1326  0 04:10 ?        00:01:49 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Xms1g -Xmx1g -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+AlwaysPreTouch -Xss1m -Djava.awt.headless=true -Dfile.encoding=UTF-8 -Djna.nosys=true -XX:-OmitStackTraceInFastThrow -Dio.netty.noUnsafe=true -Dio.netty.noKeySetOptimization=true -Dio.netty.recycler.maxCapacityPerThread=0 -Dlog4j.shutdownHookEnabled=false -Dlog4j2.disable.jmx=true -Djava.io.tmpdir=/tmp/elasticsearch.1UkoCBcT -XX:+HeapDumpOnOutOfMemoryError -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime -Xloggc:logs/gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=32 -XX:GCLogFileSize=64m -Des.path.home=/opt/elasticsearch-6.2.4 -Des.path.conf=/opt/elasticsearch-6.2.4/config -cp /opt/elasticsearch-6.2.4/lib/* org.elasticsearch.bootstrap.Elasticsearch
root       1776      1  0 04:10 ?        00:00:00 node /opt/node-v6.14.2-linux-x64/bin/http-server -p 8082 --push-state --ssl --cert /certs/cert.pem --key /certs/privatekey_new.pem .
demoadm+   1944      1  0 04:10 ?        00:00:00 bash /opt/apache-atlas-2.0.0/hbase/bin/hbase-daemon.sh --config /opt/apache-atlas-2.0.0/hbase/conf foreground_start master
demoadm+   1961   1944  0 04:10 ?        00:01:36 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Dproc_master -XX:OnOutOfMemoryError=kill -9 %p -XX:+UseConcMarkSweepGC -Dhbase.log.dir=/opt/apache-atlas-2.0.0/hbase/bin/../logs -Dhbase.log.file=hbase-demoadmin-master-guzzlemp2vm.log -Dhbase.home.dir=/opt/apache-atlas-2.0.0/hbase/bin/.. -Dhbase.id.str=demoadmin -Dhbase.root.logger=INFO,RFA -Dhbase.security.logger=INFO,RFAS org.apache.hadoop.hbase.master.HMaster start
demoadm+   2092      1  0 04:10 ?        00:00:43 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -server -Xms512m -Xmx512m -XX:NewRatio=3 -XX:SurvivorRatio=4 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=8 -XX:+UseConcMarkSweepGC -XX:ConcGCThreads=4 -XX:ParallelGCThreads=4 -XX:+CMSScavengeBeforeRemark -XX:PretenureSizeThreshold=64m -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=50 -XX:CMSMaxAbortablePrecleanTime=6000 -XX:+CMSParallelRemarkEnabled -XX:+ParallelRefProcEnabled -XX:-OmitStackTraceInFastThrow -verbose:gc -XX:+PrintHeapAtGC -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime -Xloggc:/opt/apache-atlas-2.0.0/solr/server/logs/solr_gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=9 -XX:GCLogFileSize=20M -DzkClientTimeout=15000 -DzkHost=localhost:2181 -Dsolr.log.dir=/opt/apache-atlas-2.0.0/solr/server/logs -Djetty.port=9838 -DSTOP.PORT=8838 -DSTOP.KEY=solrrocks -Duser.timezone=UTC -Djetty.home=/opt/apache-atlas-2.0.0/solr/server -Dsolr.solr.home=/opt/apache-atlas-2.0.0/solr/server/solr -Dsolr.data.home= -Dsolr.install.dir=/opt/apache-atlas-2.0.0/solr -Dsolr.default.confdir=/opt/apache-atlas-2.0.0/solr/server/solr/configsets/_default/conf -Xss256k -Dsolr.jetty.https.port=9838 -Dsolr.log.muteconsole -XX:OnOutOfMemoryError=/opt/apache-atlas-2.0.0/solr/bin/oom_solr.sh 9838 /opt/apache-atlas-2.0.0/solr/server/logs -jar start.jar --module=http
demoadm+   3029      1  1 04:11 ?        00:03:36 /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Datlas.log.dir=/opt/apache-atlas-2.0.0/logs -Datlas.log.file=application.log -Datlas.home=/opt/apache-atlas-2.0.0 -Datlas.conf=/opt/apache-atlas-2.0.0/conf -Xmx1024m -Dlog4j.configuration=atlas-log4j.xml -Djava.net.preferIPv4Stack=true -server -classpath /opt/apache-atlas-2.0.0/conf:/opt/apache-atlas-2.0.0/server/webapp/atlas/WEB-INF/classes:/opt/apache-atlas-2.0.0/server/webapp/atlas/WEB-INF/lib/*:/opt/apache-atlas-2.0.0/libext/*:/opt/apache-atlas-2.0.0/hbase/conf org.apache.atlas.Atlas -app /opt/apache-atlas-2.0.0/server/webapp/atlas


```

### In Databricks 
1. In Databricks workspace you will see new analytics cluster called guzzle-config created (if there is existing one, that continues to remain - as cluster has unique id underneath and they don't go by name)
![image](/guzzle-docs/img/docs/azure/databricks1.png)
1. Also you would notice that Guzzle Home will have got mounted in Databricks workspace (mounts in Databricks are at workspace level and NOT at cluster level)
On Databricks workspace you can create sample notebook and run it against guzzle-config or any anlaytics cluster) and ensure you see the Guzzle home mounted:
![image](/guzzle-docs/img/docs/azure/databricks2.png)

### In Storage Account
1. In storage account you will see new files added up  in container which hosts Guzzle Home
![image](/guzzle-docs/img/docs/azure/storage_account.png)


### In SQL Server databases
1. The Guzzle repository and Guzzle API table should show up in Guzzle repository database. The below ones will show up first as Guzzle Repo gets initialized
![image](/guzzle-docs/img/docs/azure/in_db1.png)
And below highlighted ones shows up when API comes up:
![image](/guzzle-docs/img/docs/azure/in_db2.png)
1. Hive metastore tables should show up in External metastore 
Before when there are no tables in this databaes
After the job starts (steps to run the jobs before :
![image](/guzzle-docs/img/docs/azure/in_db3.png)

## Once everything is set
1. Launch the Guzzle URL
![image](/guzzle-docs/img/docs/azure/final_steps_1.png)
1. And then login
![image](/guzzle-docs/img/docs/azure/final_steps_2.png)
1. Run the sample job from here
![image](/guzzle-docs/img/docs/azure/final_steps_3.png)
1. This brings up Job Cluster. This also initializes hivemetastore as the first job runs using the external meastore 
![image](/guzzle-docs/img/docs/azure/final_steps_4.png)
1. On successful completion the job should show up 
![image](/guzzle-docs/img/docs/azure/final_steps_5.png)
![image](/guzzle-docs/img/docs/azure/final_steps_6.png)


## What happens when we redo Marketplace deployment using same Azure resources multiple times
1. If the blobstorage container, contains existing Guzzle files, it will simply overwrite them when doing a fresh marketplace deploy. 
1. If databricks workspace is already containing the guzzle-config cluster, its ignored and fresh one is created. Any existing mount of guzzle blotstorage container on /mnt/guzzle in that workspace is unmounted. A new mount is done pointing to the details given in marketplace wizard 
1. Guzzle repository database tables if present in the same Azure SQL database, the deployment of Guzzle repository gets skipped (no cleanup is required - unless the database contains tables from older version of Guzzle deployment)
1. Hive metastore tables if present in the same Azure SQL database for External metastore database for Databricks, the step of deploying fresh metastore tables is skipped  (you don't need any cleanup)

## Atlas Issues
Following are the fixes of issues in Apache Atlas
1. By default marketplace starts Atlas using the root. We need to modify Guzzle startup script to change this to non-root account. We can use the account used during the VM creation (demoadmin or appropriate user). Once this is chagnd, restart Guzzle VM

![image](/guzzle-docs/img/docs/azure/atlas1.png)

```shell
sudo bash
chown demoadmin:demoadmin -R /opt/apache-atlas-2.0.0
vi /opt/guzzlescript/guzzle-startup-script.sh

# Update the Atlas startup command as per below
 nohup sudo --preserve-env=PATH -HEu demoadmin bash -c  "/opt/apache-atlas-2.0.0/bin/atlas_start.py" > /guzzle/logs/atlas.out &

```
![image](/guzzle-docs/img/docs/azure/atlas2.png)
2. Edit the /guzzle/conf/atlas.yml file to remove the below entirely  
```yml
hive:
  jdbc_url: jdbc:spark:....
```
The revised file should look as per below:

![image](/guzzle-docs/img/docs/azure/atlas3.png)
Restart the Guzzle VM from Azure Portal and wait for 10 minutes for all the services to come up

3. Atlas sync only supported for Local file system
- Atlas sync is currently only supported local file system, Hive, Delta and JDBC sources. It does not support all the cloud file system
- In databricks guzzle home mounted under /dbfs/mnt/guzzle while in Guzzle VM its mounted under /guzzle.
- When referring to the guzzle home and source file there in one has to use /dbfs/mnt/guzzle
- Create symbolic link in Guzzle VM that points to the same LFS (local file system) path as Databricks run below command (first command is to switch to root)
```shell
demoadmin@guzzlemp2vm:/guzzle/test-data$ sudo bash
root@guzzlemp2vm:/guzzle/test-data# mkdir -p /dbfs/mnt/guzzle
root@guzzlemp2vm:/guzzle/test-data# cd /dbfs/mnt/guzzle/
root@guzzlemp2vm:/dbfs/mnt/guzzle# ln -s /guzzle/test-data
```
**Note:** This step is not required if the blob storage where source files are present in same directory on Guzzle VM and Databricks.

4. Wild card (multiple files are not supported when retrieving the column list for Atlas sync)
- In the job config use specific file names like users2.csv instead of user*.csv 
5. Update the user and password for ph_hive (or appropriate hive or delta physical connection with username as "token" and password as API access token retrieved from Databricks workspace)

![image](/guzzle-docs/img/docs/azure/atlas4.png)
6. Run the scrip to create Guzzle metadata type (this is only if when you don't see guzzle metatypes like guzzle_dataset , guzzle_process etc in Atlas)
```shell
sudo bash
/opt/guzzlescript/create-atlas-types.sh
```

## Using ADLSv2 as Storage for Delta and Hive tables and usage of Databricks Secrets
1. Create ADLS storage account and file system
1. Grant the Blob storage contributor permission to one of the Service Principal (you can use existing service principal that is being used for Azure AD SSO)
1. Create Azure key vaults to store the secrets (in this case the Service principal client id and client secret) (follow the link here: https://docs.microsoft.com/en-us/azure/key-vault/quick-create-portal ) or video
1. Create Databricks secret scope backed by Azurekey vault (follow Video) or this link: https://docs.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes#--create-an-azure-key-vault-backed-secret-scope 
1. Mount this storage account on Databricks workspace under /mnt/data  - we will use plain notebook to specify the secrets of Service principal. I have used Python notebook to do it. Notice that I have used Databricks secrete backed by 

```python
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope = "guzzlevm2scope", key = "guzzlemv2spclient"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope = "guzzlevm2scope", key = "guzzlemv2spclientsec"),
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/bc5c7327-b12e-48db-a856-175591ecd2f0/oauth2/token"}

dbutils.fs.mount(
  source = "abfss://datalake1@adlsv2guzzlecommon.dfs.core.windows.net/data",
  mount_point = "/mnt/data",
  extra_configs = configs)
```
1. Verify the ADLS mount is working fine and you are able list the files. Do take not that dbfs mount is /mnt/data ,which implies the mount on Unix (or local file system representation) will be /dbfs/mnt/data
1. Now, Create a database "test" in Databricks and point to the /mnt/data/test as the location (do take note that folder test if not present then Databricks will  create when creating database) . With this all the tables in database "test" shall go into the folder /mnt/data/test in DBFS which in turn then goes into datalake1 container (aka filesystem) in the ADLSgen2 storage account: adlsv2guzzlecommon. Also create sample table so and insert some data into it
```sql
%sql
create database test location '/mnt/data/test';
use test;
create table t1(i int);
insert into t1 values(1);
```
When going back to ADLS file explorer you should notice a new sub-folder test and child folder in it t1 will have been created confirming that table has got corrected created in the ADLS stroage
![image](/guzzle-docs/img/docs/azure/adls_delta_storage.png)
1. Go to Guzzle and define new logical and physical end point pointing to the this new database "test". You can create both Hive and Delta endpoints against the same database "test" and the tables will be stored as delta or hive tables based on which end point is used or target


## Securing Guzzle Deployment
### VM and SSO
1. Enable azure SSO for Guzzle
- Ensure redirect URL is put in Authentication tab in App Registration "https://<<hostname[.southeastasia.cloudapp.azure.com]>>:8082/oauth/microsoft"
![image](/guzzle-docs/img/docs/azure/securing1.png)
- Add your Azure AD account as admin role. Put the password which is complex or random as you will not need it. Make sure you are able to login through

![image](/guzzle-docs/img/docs/azure/securing2.png)

- Delete the Native Admin account from Guzzle repository. Login to SQL server and run below commands against guzzle Repoisotyr database
```sql
delete from user_authorities  where user_id = 1;
delete from users where id = 1;
```
1. Enable Firewalls for Guzzle VM
- Guzzle VM : Only open selected ports for external traffic : 9090,  8082, 21000 and 22)
![image](/guzzle-docs/img/docs/azure/securing3.png)
- Outbound traffic will have following rules - internet access will be required (till private endpionts can be used for all the Azure pass services):
![image](/guzzle-docs/img/docs/azure/securing4.png)
1. Run Guzzle services from non root account and account which has no sudo access. Here is what is required  to use a new account "guzzle" to run all the Guzzle services. Do take note that original account used for VM creation is what should be used to login to the VM when required so that appropriate commands can be used to run using sudo permission :
```shell
sudo bash
# Stop all the services
kill -9 `ps aux | grep '[a]pi-0.0.1-SNAPSHOT.jar' | awk '{print $2}'`
kill -9 `ps aux | grep '[e]lasticsearch-6.2.4' | awk '{print $2}'`
kill -9 `ps aux | grep '[h]ttp-server' | awk '{print $2}'`
kill -9 `ps aux | grep '[a]tlas' | awk '{print $2}'`
# Verify no guzzle services are running except blobfuse using following
ps -ef | grep "[g]uzzle\|[n]ode\|[e]lastic\|[a]tlas"

# Create a new user guzzle. Provide relevant details prompted including a complex password for this account. 
adduser guzzle

# Change the ownership of /opt/apache-atlas-2.0.0 and /opt/elasticsearch-6.2.4 to guzzle:guzzle
chown -R guzzle:guzzle /opt/apache-atlas-2.0.0
chown -R guzzle:guzzle /opt/elasticsearch-6.2.4
```
- update the /opt/guzzlescript/guzzle-startup-script.sh to point all the service start using guzzle account. You can take the backup using the command "cp /opt/guzzlescript/guzzle-startup-script.sh /opt/guzzlescript/guzzle-startup-script.sh.ori"
```shell
echo "guzzle startup script execution started"

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export GUZZLE_HOME=/guzzle
export PATH=/opt/guzzlescript/:/opt/elasticsearch-6.2.4/bin:/opt/node-v6.14.2-linux-x64/bin:/opt/spark-2.4.5-bin-hadoop2.7/bin:$PATH
export MANAGE_LOCAL_HBASE=true
export MANAGE_LOCAL_SOLR=true

blobfuse /guzzle --tmp-path=/mnt/blobfusetmp -o allow_other --config-file=/root/fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 --file-cache-timeout-in-seconds=10

nohup sudo --preserve-env=PATH -HEu guzzle bash -c "/opt/elasticsearch-6.2.4/bin/elasticsearch" > /guzzle/logs/elasticsearch.out &

cd /guzzle/api/
nohup sudo --preserve-env=PATH -HEu guzzle bash -c "java -Dloader.path=/guzzle/api/libs -jar api-0.0.1-SNAPSHOT.jar" > /dev/null &

cd /guzzle/web/
nohup sudo --preserve-env=PATH -HEu guzzle bash -c "http-server -p 8082 --push-state --ssl --cert /certs/cert.pem --key /certs/privatekey_new.pem" . > /guzzle/logs/web.out &

if [[ "yes" == "yes" ]]; then
  nohup sudo --preserve-env=PATH -HEu guzzle bash -c "/opt/apache-atlas-2.0.0/bin/atlas_start.py" > /guzzle/logs/atlas.out &
fi

echo "guzzle startup script execution completed"
```
![image](/guzzle-docs/img/docs/azure/securing5.png)
![image](/guzzle-docs/img/docs/azure/securing6.png)


```shell
sudo bash
# Delete spring.log
rm /tmp/spring.log
# Start Guzzle service
 /opt/guzzlescript/guzzle-startup-script.sh
```
1. Change the permission of the fuse config to 400
```shell
sudo bash
cd /root/
chmod 400 fuse_connection.cfg
ls -ltrh
```
![image](/guzzle-docs/img/docs/azure/securing7.png)
- Recommended to restart Guzzle VM which should restart all the services using newly created guzzle account
3. Enable Network security for PAAS services - Azure SQL Server
3. Enable Network security for PAAS services - Storage accounts (blob and ADLS if you are using that)

### Azure Databricks security
1. Working with Databricks Secrets
