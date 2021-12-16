#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 20:47:53 2021

@author: William
"""

import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine, event
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData, DDL


MYSQL_HOSTNAME = '20.85.233.248' 
MYSQL_USER = 'dba'
MYSQL_PASSWORD = 'ahi2021'
MYSQL_DATABASE = 'e2e'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)
meta = MetaData()
meta.reflect(bind=engine)
meta.tables.keys()
'''
Initially a clean slate; output will show as follows: 
    Out[7]: dict_keys([])
'''

h1n1 = pd.read_csv('/Users/William/Desktop/H1N1_Flu_Vaccines.csv')
h1n1.to_sql('H1N1_Flu_Vaccines', con=engine, if_exists ='append') 

test = pd.read_sql('select * from newdatabase.H1N1_Flu_Vaccines', engine)
'''
Dataframe shows up means that h1n1 is now within MySQL database
Rerun meta.reflect & meta.tables.keys() to show that it is within the database:
    Out[13]: dict_keys(['H1N1_Flu_Vaccines'])
''' 

Base=declarative_base()
    
h1n1trigger = DDL("""
delimiter $$

CREATE TRIGGER H1N1_concern_trigger 
BEFORE INSERT ON e2e.H1N1_Flu_Vaccines
FOR EACH ROW
BEGIN
IF NEW.h1n1_concern >= 3 THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'H1N1 concern should be a numerical value between 0 and 3. Please try again.';
END IF;
END; 

$$
""")

event.listen(Base.metadata, 'after_create', h1n1trigger)

