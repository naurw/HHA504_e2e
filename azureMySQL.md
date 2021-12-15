#End to End (E2E) Deployment of Azure Instance(s) with MySQL
###1. Sign in / create an account at https://azure.microsoft.com/en-us/
###2. Navigate to Virtual Machines 
###3. Select Create + Virtual Machine 
###4. Designate system preferences and specifications needed for deployment(s)
###5. Review and create virtual machine(s)
###6. Return to current virtual machine(s) post deployment
###7. Select current virtual machine and navigate to Networking
###8. Select Add Inbound Port Rule 
###9. Designate port preferences and specifications for MySQL (port 3306)
###10. Select Add
##OPTIONAL: For changing IP configurations (static vs dynamic)
###11. Navigate to current virtual machine(s) 
###12: Select Networking and navigate to the link next to Network Interface 
###13. Navigate to IP Configurations 
###14. Select virtual machine(s) that you want to configure 
###15. Select dynamic / static and select save to exit 


#Accessing Virtual Machine via Terminal 
###1. ssh (USER)@(IP_ADDRESS) --IP address can be found in the overview page of each instance 
###2. Enter password after fingerprinting (Y) localhost 
###3. sudo apt-get update
###4. sudo apt-get install mysql-server mysql-client 
###5. sudo service ssh restart  
###6. sudo nano /etc/mysql/mysql.conf.d/mysql.cnf
####- bind address --> 0.0.0.0
####- server_id --> 1 
####- log_bin --> Remove # 
####- bin_log_do_db --> Remove # 
####- control + O to save changes 
####- control + x to exit 
###7. sudo service mysql restart 

