# End to End (E2E) Deployment of Azure Instance(s) with MySQL
### READ ME BEFORE PROCEEDING: 
##### codes => FIRST LETTER is LOWERCASE 
##### Instructions => FIRST LETTER is UPPERCASE 

# A) Creating and Launching Instance(s)
### 1. Sign in / create an account at https://azure.microsoft.com/en-us/
### 2. Navigate to Virtual Machines 
### 3. Select Create + Virtual Machine 
### 4. Designate system preferences and specifications needed for deployment(s)
#### - Choose either SSH key (will require addtional steps not listed) or simple user/password configuration 
#### - For this demonstration, best practices will be *waived* in favor of simplicity of access 
### 5. Review and create virtual machine(s)
### 6. Return to current virtual machine(s) post deployment
### 7. Select current virtual machine and navigate to Networking
### 8. Select Add Inbound Port Rule 
### 9. Designate port preferences and specifications for MySQL (port 3306)
### 10. Select Add
## **OPTIONAL**: For changing IP configurations (static vs dynamic)
### 11. Navigate to current virtual machine(s) 
### 12: Select Networking and navigate to the link next to Network Interface 
### 13. Navigate to IP Configurations 
### 14. Select virtual machine(s) that you want to configure 
### 15. Select dynamic / static and select save to exit 


# B) Accessing Instance(s) via Terminal
### 1. ssh (USER)@(IP_ADDRESS) --IP address can be found in the overview page of each instance 
### 2. Enter password after fingerprinting (Y) localhost 
### 3. sudo apt-get update
### 4. sudo apt-get install mysql-server mysql-client 
### 5. sudo service ssh restart  
### 6. sudo nano /etc/mysql/mysql.conf.d/mysql.cnf
#### - bind address --> 0.0.0.0
#### - server_id --> 1 
#### - log_bin --> Remove hastag
#### - bin_log_do_db --> Remove hastag
#### - control + o to save changes 
#### - control + x to exit 
### 7. sudo service mysql restart 
### 8. sudo mysql 
### 9. create user 'USERNAME'@'%' identified by 'PASSWORD'; 
#### - Creating database administrator account--refrain from using root
#### - This is creating a user and password within MySQL server--different from the credentials for logging into the virtual machine
### 10. select * from mysql.user; 
#### - Verify the creation of the user 
### 11. grant all privileges on *.* 'USERNAME'@'%' with grant option
### 12. flush privileges; 
### 13. show grants for USER \G
#### - Verify the grants have been implemented into the user
### 14. exit;
### 15. mysql -u USER -p 
#### - Log in with newly created database administrator account 
### 16. show database; 
### 17. create database INSERTNAME; 
#### - Verify creation of database with step 16 


# C) Create table into database in MySQL Instance via Python or SQL
## **Method 1:** Python -> Please see attached .py file in this repo for an example 
### 1. Import packages 
### 2. Connect to MySQL instance 
### 3. Test connection by displaying tables 
### 4. Load .csv file 
### 5. Confirm table has been placed into designated database 
## **Method 2:** SQL
### 1. mysql -u USER -p 
### 2. show databases; 
### 3. use INSERTNAME; 
### 4. create table if not exists TABLENAME (col1 INT auto_increment primary key, col2 varchar(50) not null, col3...) engine = innodb 
### 4. show tables; 


# D) Create a trigger in MySQL Instance via via Python or SQL
## **Method 1:** Python** -> Please see attached .py file in this repo for an example 
### 1. Import packages  
### 2. Connect to MySQL instance 
### 3. Test connection 
### 4. Create trigger 
### 5. Confirm trigger has been placed into designated database 
## **Method 2:** SQL
### 1. mysql -u USER -p 
### 2. show databases; 
### 3. use INSERTNAME; 
### 4.  select * from TABLENAME limit 10;
###     delimiter $$
###     create trigger TRIGGERNAME before insert on TABLENAME
###     for each row
###     begin if new.alert >=3 then
###     signal sqlstate '45000'
###     set message_text = 'NAMEOFTABLE concern should be a numerical value between 0 and 3. Please try again.'
###     ;end if;
###     end; $$
### 5. show triggers; 


# E) Creating Cold Backup (Requires 2 Instances)
### 1. Repeat Part A) but with separate credentials for new virtual machine 
### 2. Follow Part B) until step 8 
### 3. Log out of backup instance and log in to production/host instance 
### 4. sudo mysqldump -- all databases> dump.sql
### 5. ls 
#### - Locate the present working directory of the host instance 
#### - Copy directory 
### 6. Log out of host instance and log in to the backup instance 
### 7. scp dump.sql USERNAME@2ND IP ADDRESS:/home/USERNAME
### 8. ls
#### - Verify the copied dump.sql within backup instance 

