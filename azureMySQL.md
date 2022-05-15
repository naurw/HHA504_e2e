## End to End (E2E) Deployment of Azure Instance(s) with MySQL
### **NOTE**: 
### All the bullets/steps are listed in *sequential* *order*.
### Key parts will be `highlighted` as such. 
> Codes will appear as such. 


#### A) Creating and Launching Instance(s)
* Sign in and create an account @ https://azure.microsoft.com/en-us/ 
* Navigate to `Virtual Machines`
* Select `Create + Virtual Machine` 
* Designate system preferences and specifications needed for deployment(s)
    * Choose either `SSH key` (will require addtional steps not listed) ***OR*** simple `user/password configuration `
        * For this demonstration, best practices will be ***waived*** in favor of simplicity of access 
* Review and create virtual machine(s)
* Return to current virtual machine(s) post deployment
* Select current virtual machine and navigate to `Networking`
* Select `Add Inbound Port Rule `
* Designate port preferences and specifications for `MySQL` 
    * Port 3306 
* Select Add
* **OPTIONAL**: For changing IP configurations (static vs dynamic)
    * Navigate to current virtual machine(s) 
    * Select `Networking` and navigate to the link next to `Network Interface` 
    * Navigate to `IP Configurations `
    * Select virtual machine(s) that you want to configure 
    * Select dynamic / static and select save to exit 

#### B) Accessing Instance(s) via Terminal
> ssh (USER)@(IP_ADDRESS) 
> - IP address can be found in the `Overview` page of each instance 
> - Enter password after fingerprinting 
>   - (Y) localhost 
> sudo apt-get update

> sudo apt-get install mysql-server mysql-client 
    
> sudo service ssh restart  
    
> sudo nano /etc/mysql/mysql.conf.d/mysql.cnf
> - bind address 
>   - change to 0.0.0.0
> - server_id 
>   - change to 1 
> - log_bin 
>   - remove hastag/uncomment 
> - bin_log_do_db 
>   - remove hastag/uncomment
> - control + o to save changes 
> - control + x to exit 

> sudo service mysql restart 

> sudo mysql 

> create user 'USERNAME'@'%' identified by 'PASSWORD'; 
> - Creating database administrator account--refrain from using root
> - This is creating a user and password within MySQL server--different from the credentials for logging into the virtual machine

> select * from mysql.user; 
> - verify the creation of the user 

> grant all privileges on *.* 'USERNAME'@'%' with grant option

> flush privileges; 

> show grants for USER \G
> - Verify the grants have been implemented into the user

> exit;

> mysql -u USER -p 
> - Log in with newly created database administrator account 

> show database; 

> create database INSERTNAME; 
> - verify creation of database with step 16 

#### C) Creating a table in MySQL DB via Python or SQL
* **METHOD 1:** Python -> Please see attached .py file in this repo for an example 
    * Import packages 
    * Connect to MySQL instance 
    * Test connection by displaying tables 
    * Load .csv file 
    * Confirm table has been placed into designated database 
* **METHOD 2:** SQL
    > mysql -u USER -p 

    > show databases; 

    > use INSERTNAME; 

    > create table if not exists TABLENAME (col1 INT auto_increment primary key, col2 varchar(50) not null, col3...) engine = innodb 

    > show tables; 


#### D) Create a trigger in MySQL DB via Python or SQL
* **METHOD 1:** Python -> Please see attached .py file in this repo for an example 
    * Import packages  
    * Connect to MySQL instance 
    * Test connection 
    * Create trigger 
    * Confirm trigger has been placed into designated database 
* **METHOD 2:**  SQL
    > mysql -u USER -p 

    > show databases; 

    > use INSERTNAME; 
    
    > select * from TABLENAME limit 10;

    > delimiter $$
    * `create trigger TRIGGERNAME before insert on TABLENAME`
    * `for each row`
    * `begin if new.alert >=3 then`
    * `signal sqlstate '45000'`
    * `set message_text = 'NAMEOFTABLE concern should be a numerical value between 0 and 3. Please try again.'`
    * `;end if;`
    * `end; $$`

    > show triggers; 


#### E) Creating Cold Backup (Requires 2 Instances)
* Repeat Part A) but with separate credentials for new virtual machine 
* Follow Part B) until step 8 
* Log out of backup instance and log in to production/host instance 
    > sudo mysqldump DATABASE_NAME> dump.sql
    > ls 
    > - Locate the present working directory of the host instance 
* Log out of host instance and log in to the backup instance
    - Copy directory of backup instance
* Log out of backup instance and log in to host instance 
    > scp dump.sql BACKUP_INSTANCE_NAME@IP_ADDRESS:COPIED_DIRECTORY 
    > ls
    > - Verify the copied dump.sql within backup instance 
