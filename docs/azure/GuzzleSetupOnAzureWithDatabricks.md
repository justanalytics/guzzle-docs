---
id: azure_manual
title: Installing Guzzle on Azure with Databricks
sidebar_label: Installing on Azure Manually
---


## Guzzle Setup Step By Step Guide

### Index
---
1. [STEP 1: Create Resources](#step1)
    1. [Blob Storage](#step1.1)
    2. [Databricks](#step1.2)
    3. [SQL Server](#step1.3)
    4. [SQL Database](#step1.4)
    5. [Linux VM](#step1.5)
2. [STEP 2: Databricks configuration](#step2)
3. [STEP 3: Guzzle VM configuration](#step3)
4. [STEP 4: Start Guzzle](#step4)
5. [STEP 5: Final steps](#step5)



---
<div class="page"/>

<a name="step1"></a>
### STEP 1: Create Resources
Required resources for guzzle installation are as follows:
>Please create Guzzle related resources in same region.

1.  **Blob Storage**: For storing Guzzle binaries
2.  **Databricks**: Guzzle uses Databricks Spark cluster for running jobs
3.  **SQL Server and Database**: For storing Guzzle jobs and api related data
4.  **Linux VM**: For Guzzle API and UI installation

**Create each resources with appropriate details as follows:**
<a name="step1.1"></a>
#### 1. Blob Storage

- Select appropriate **Subscription** & **Resource group**
- **Storage account name**: [preferred name]
- **Location**: [preferred location]
- **Performance**: Standard
- **Account kind**: StorageV2 (general purpose v2)
- **Replication**: Locally-redundant storage (LRS)
- **Access tier**: Hot
- **Create a container**, named <container_name>
- Save container name, storage account name and account keys from **Access keys** section somewhere for further use.<a name="blob_storage_info"></a>

    >![storage keys](/guzzle-docs/img/docs/azure-manual/storageaccesskeys.png)



<div class="page"/>

<a name="step1.2"></a>
#### 2. Databricks

- **Workspace name**:[preferred-name]
- Select appropriate **Subscription** & **Resource group**
- **Location**: [preferred-location]
- **Pricing Tier**: Premium
- Go to Databricks resources and save the Url somewhere for further use.<a name="databricks_url"></a>

    >![databricks_url](/guzzle-docs/img/docs/azure-manual/databricks.png)

- Create a cluster with in Databricks workspace with following configurations:
    + **Databricks runtime version**: 5.4 (includes Apache Spark 2.4.3, Scala 2.11) 
    + **Python version**: 3
    + **Enable Autoscaling**: false
    + Terminate after **60** minutes of inactivity
    + **Worker Type**: [as per requirements]
    + **Driver Type**: Same as worker

- Once the cluster is created, click on the cluster and then save the cluster-id from the url somewhere for further use.<a name="databricks_cluster_id"></a>

    >![cluster-id](/guzzle-docs/img/docs/azure-manual/clusters.png)

<div class="page"/>

- Create access token:
    1. Select User settings
    
        >![user settings](/guzzle-docs/img/docs/azure-manual/databricks_access_token.png)

    2. Click on Generate Token and provide comment and lifetime for access token. Click on Generate.
    
        >![generate token](/guzzle-docs/img/docs/azure-manual/generate_token.png)
    
    3. Copy the token somewhere as it will not be accessible after clicking Done. Click Done<a name="databricks_token"></a>.
    
        >![copy token](/guzzle-docs/img/docs/azure-manual/copy_token.png)  

<div class="page"/>

<a name="step1.3"></a>
#### 3. SQL Server

- Select appropriate **Subscription** & **Resource group**
- **Server name**: [preferred name]
- **Location**: [preferred location]
- **Server admin login**: [username]
- **Password**: [password]

<a name="step1.4"></a>
#### 4. SQL Database

- Select appropriate **Subscription** & **Resource group**
- **Database name**: [preferred name]
- **Server**: Select the already created SQL server from drop down
- **Want to use SQL elastic pool?**: No
- **Compute + storage**: As per the requirement

<a name="step1.5"></a>
#### 5. Linux VM

- Select appropriate **Subscription** & **Resource group**
- **Virtual machine name**: Guzzle
- **Region**: Southeast Asia
- **Availability options**: keep default
- **Image**: Ubuntu Server 18.04 LTS
- **Size**: B2s
- **Authentication type**: Password
- **Username**: guzzle
- **Password**: [preferred password]
- **Public inbound ports**: Allow selected ports
- **Select inbound ports**: HTTP, HTTPS, SSH

---

<div class="page"/>

<a name="step2"></a>
### STEP 2: Databricks configuration

1. Launch the databricks workspace.
2. Inside Workspace>shared create Guzzle folder.

    >![Guzzle folder](/guzzle-docs/img/docs/azure-manual/guzzle_folder.jpg)

3. Create notbook names guzzle init and create cells as follows:
    1. Replace placeholders with appropriate values saved earlier. Look [here](#blob_storage_info)
        ```scala
        dbutils.fs.mount(source = "wasbs://<container-name>@<storage-name>.blob.core.windows.net/",
        mountPoint = "/mnt/guzzle",
        extraConfigs = Map("fs.azure.account.key.<storage-name>.blob.core.windows.net" -> "<storage-key>"))
        ```
    2. Check if successfully mounted.
        ```sh
        %sh
        ls -ltrh /dbfs/mnt/guzzle
        ```

    <div class="page"/>

    3. Create init script.
        ```sh
        %sh
        echo "log4j.appender.RollingAppender=org.apache.log4j.DailyRollingFileAppender
        log4j.appender.RollingAppender.layout=org.apache.log4j.PatternLayout
        log4j.appender.RollingAppender.DatePattern='.'yyyy-MM-dd
        log4j.appender.RollingAppender.layout.ConversionPattern=[%p] %d %c %M - %m%n
        log4j.logger.com.justanalytics=INFO, RollingAppender
        " > /dbfs/guzzle-log4j.properties

        mkdir -p /dbfs/databricks/initscript
        echo "#!/bin/bash
        cat /dbfs/guzzle-log4j.properties >> /databricks/spark/dbconf/log4j/driver/log4j.properties
        cat /dbfs/guzzle-log4j.properties >> /databricks/spark/dbconf/log4j/executor/log4j.properties
        " > /dbfs/databricks/initscript/init.sh
        ```

4. Go to the cluster and click on **Edit**.
5. Click on **Advanced Options** and add following line in **Environment Variables**
    ```
    GUZZLE_HOME=/dbfs/mnt/guzzle/guzzle
    ```
    >Above GUZZLE_HOME is as per default directory structure. Azure Databricks clusters supposed to have only GUZZLE_HOME environment variable which points to guzzle configs,jars etc. and not required GUZZLE_PRODUCT_HOME which points to api and web modules.
6. Go to **Init Scripts** tab and add `databricks/initscript/init.sh`.
    
    >![initscript](/guzzle-docs/img/docs/azure-manual/initscript.png)

7. Restart the cluster.

---

<div class="page"/>

<a name="step3"></a>
### STEP 3: Guzzle VM configuration

1. Upload guzzle(tar.gz), tools(tar.gz) and neccesary jdbc connector provided with this document.
2. Mount Blob Container:
    1. Install blob fuse by running following commands:
        ```sh
        wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb
        sudo dpkg -i packages-microsoft-prod.deb
        sudo apt-get update
        sudo apt-get install blobfuse fuse -y
        echo "user_allow_other" | sudo tee -a /etc/fuse.conf
        ```
    2. Create dir /mnt/blobfusetmp and provide permissions:
        ```sh
        sudo mkdir /mnt/blobfusetmp
        sudo chown guzzle /mnt/blobfusetmp
        ```
    3. Create fuse_connection.cfg file. Replace placeholders with appropriate values. Look [here](#blob_storage_info):
        ```sh
        echo "accountName <storage name>
        accountKey <storage-key>
        containerName <container-nameguzzlehome>" > /home/<user>/fuse_connection.cfg

        chmod 777 /home/<user>/fuse_connection.cfg
        ```
    4. Create guzzle directory to mount the blob storage:
        > Some codes does not get copied exactly as shown. Make sure to check before running it.
        ```sh
        sudo mkdir -m 777 /guzzle
        sudo -H -u <user> bash -c "blobfuse /guzzle --tmp-path=/mnt/blobfusetmp -o allow_other --config-file=/home/<user>/fuse_connection.cfg -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 --file-cache-timeout-in-seconds=10"
        ```
    5. Run below code and check in blob storage if the file **a.log** was created:
        ```sh
        cd /guzzle
        echo "test" > a.log
        ```


3. Extract files:
    ```sh
    cd ~
    tar xzf guzzle-<version>.tar.gz -C /guzzle/ --strip-components=1
    ```

4. Install Java by running following commands: 
    ```sh
    sudo apt install openjdk-8-jre-headless -y
    sudo apt install openjdk-8-jdk-headless -y
    ```

5. Set environment variables.
    >Replace &lt;version&gt; with appropriate version

    ```sh
    cd ~
    echo "export GUZZLE_HOME=/guzzle/guzzle" >> .bashrc
    echo "export GUZZLE_PRODUCT_HOME=/guzzle" >> .bashrc
    echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/"
    source .bashrc
    ```
    Run `echo $GUZZLE_HOME` to check if the variable was set successfully.
    Environment variable GUZZLE_HOME & GUZZLE_PRODUCT_HOME supposed to point to guzzle core and guzzle api modules respectively.
    
    GUZZLE_HOME should contain following directories from guzzle setup. However, directory like 'logs' can be moved afterwards with admin settings using guzzle app or directly updating related property in guzzle.yml.

        - bin
        - conf
        - hive-connectors
        - libs
        - logs
        - scripts

    GUZZLE_PRODUCT_HOME must contain following directories from guzzle setup.

        - api
        - web


6. Install MySQL
    >Run following commands to install mysql:

    ```sh
    sudo apt-get update
    sudo apt-get install mysql-server -y
    ```

<div class="page"/>

7. Configure MySQL
    1. Run `sudo mysql_secure_installation` and follow these steps:
        - Enter **Y** for using VALIDATE PASSWORD plugin.
        - Select **1** for MEDIUM or **2** for STRONG.
        - Enter your password and confirm it.
        - Enter **Y** to continue with provided password.
        - Enter **Y** to remove anonymous users.
        - Enter **N** to allow remote login.
        - Enter **Y** to remove test database.
        - Enter **Y** to reload privilege table.
    
    2. Login to mysql by simply running `sudo mysql` and execute following commands one by one. 
        >Make sure you change the password in **ALTER USER & CREATE USER** queries.

        ```sql
        ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password given in the above configuration>';
        FLUSH PRIVILEGES
        CREATE USER 'guzzle'@'%' IDENTIFIED BY '<your-password>';
        GRANT ALL PRIVILEGES ON *.* TO 'guzzle'@'%' WITH GRANT OPTION;
        CREATE DATABASE guzzle;
        ```
        >Run `SELECT user,authentication_string,plugin,host FROM mysql.user;` in mysql to look at the user details.

    3. More configurations:
        - Run `sudo systemctl enable mysql` to start mysql automatically whenever the VM is rebooted.
        - Run `sudo ufw allow mysql` to make it accessible from outside the VM and run `sudo service ufw restart` to apply the changes.
        - Open **/etc/mysql/mysql.conf.d/mysqld.cnf** file and comment the line starting with **bind-address**.
        - Finally restart mysql by running `sudo service mysql restart`.

<div class="page"/>

8. Configure guzzle:
    1. Go to the Guzzle VM resource on Azure and configure the DNS name. After configuration it will look like this. Save the DNS somewhere for further use <a name="guzzle_vm_dns"></a>:
        
        >![dns name](/guzzle-docs/img/docs/azure-manual/DNSName.png)
 
    2. Open **/guzzle/conf/instance/spark/spark_azure_databricks.yml** and edit as follows:
        - Replace following values with the values saved earlier during databricks creation.
            + *&lt;databricks-url&gt;* Look [here](#databricks_url)
            + *&lt;access-token&gt;* Look [here](#databricks_token)
            + *&lt;cluster-id&gt;* Look [here](#databricks_cluster_id)
    
        ```yaml
        version: 1
        run_mode: "azure-databricks"
        properties:
          api_url: "<databricks-url>"
          auth_token: "<access-token>"
          cluster_id: "<cluster-id>"
          type: "existing-cluster"
          dbfs_guzzle_dir: "dbfs:/mnt/guzzle"
        ```

    <div class="page"/>

    3. Update **GUZZLE_HOME/conf/guzzle.yml**. It should look similar to the one given below. 
        >Make sure to change the mysql password and **DNS_name** ([here](#guzzle_vm_dns)) in jdbc_url:

        ```yaml
        version: 1
        database:
          type: jdbc
          properties:
            jdbc_url: jdbc:mysql://<DNS_name>:3306/guzzle?autoReconnect=true
            username: guzzle
            password: <your-password>
        context_columns: [system, location]
        stages: [STG, FND, SNP, CALC, REP, OUT]
        default_spark: spark_azure_databricks
        java:
          classpath: ".:/usr/hdp/current/hive-client/lib/hive-metastore.jar:/usr/hdp/current/hive-client/lib/hive-service.jar:/usr/hdp/current/hive-client/lib/hive-exec.jar:/usr/hdp/current/hive-client/lib/hive-jdbc.jar:/usr/hdp/current/hadoop-hdfs-client/hadoop-hdfs.jar:/usr/hdp/current/hadoop-client/hadoop-common.jar"
        guzzle:
          hive:
            storage_format: ORC
          log:
            dir: /guzzle/logs
        api:
          url: http://localhost:9090
        ```

    <div class="page"/>

    4. Update **GUZLE_PRODUCT_HOME/api/guzzle-api.yml**. It should look similar to the one give below:
        >Make sure to change the mysql password and DNSName ([here](#guzzle_vm_dns)):
        
        ```yaml
        application:
          authentication:
            type: database
        server:
          port: 9090
        database:
          type: "jdbc"
          properties:
            jdbc_url: "jdbc:mysql://<DNS_name>:3306/guzzle?autoReconnect=true"
            username: "guzzle"
            password: "<your-password>"
        context_columns: [system, location]
        stages: [STG, FND, SNP, CALC, REP, OUT]
        ```

    5. Update following variables in **script** tag inside **GUZLE_PRODUCT_HOME/web/index.html** as follows. Replace &lt;DNS_name&gt; with the DNS of the Guzzle VM saved earlier ([here](#guzzle_vm_dns)):
        - **window.API_URL**: "http://&lt;DNS_name&gt;:9090"
        - **window.API_DOMAIN**: "&lt;DNS_name&gt;"

9. Initialize Guzzle Database in MySQL:
    - Run following command to initialize the database:
        ```sh
        java -cp $GUZZLE_HOME/libs/*:$GUZZLE_HOME/libs:$GUZZLE_HOME/bin/* com.justanalytics.guzzle.common.DatabaseInitializer
        ```
    <div class="page"/>

---

<div class="page"/>

<a name="step4"></a>
### STEP 4: Start Guzzle

1. Start Guzzle API:
    ```sh
    cd $GUZZLE_PRODUCT_HOME/api
    nohup java -jar api-0.0.1-SNAPSHOT.jar &
    ```

2. Start Guzzle UI:
    
    Install nodejs, npm & serve to run the react app
    ```sh
    sudo apt-get install nodejs && sudo apt-get install npm && sudo npm install -g serve
    ```
    ```sh
    cd $GUZZLE_PRODUCT_HOME/web
    nohup serve -p 8082 -s . &
    nohup http-server -p 8082 --push-state --ssl --cert /guzzle/certs/cert.pem --key /guzzle/certs/privatekey_new.pem &
    ```

    >NOTES:

    >To look at the output of nohup `tail -f nohup.out` can be used if filename is not explicitly specified. Use &lt;filename&gt;.out instead.<br/><br/>
    >To look at the running java programs like elasticsearch or guzzle, use `jps -lvm`. To kill a program use `sudo kill -9 <process-id>`.
---

<div class="page"/>

<a name="step5"></a>
### STEP 5: Final steps

1. Go to the Guzzle VM resource>Networking and add **8082, 9090, 3306** in the inbound rules as shown here.
    >![inbound port](/guzzle-docs/img/docs/azure-manual/guzzle_vm_networking.png)

2. Now you should be able to access the guzzle ui through **http://&lt;DNS_name&gt;:8082**


Notes:
>1. If **spark-hive-connector.jar** isn't there in $GUZZLE_HOME/bin, copy and paste it from $GUZZLE_HOME/hive-connector.
>2. make sure **$GUZZLE_HOME/conf/default/file-template** does **exist**, create an empty one otherwise, wi