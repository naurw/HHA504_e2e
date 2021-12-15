#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 23:37:47 2021

@author: William
"""

# =============================================================================
# Uploading a table and creating a simple trigger into production instance via MySQL for testing purposes
# - Instance can only run once; restart kernel if need be 
# - This is a TESTING template for future iterations 
# =============================================================================

import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine, event
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData, DDL


MYSQL_HOSTNAME = '20.85.233.248' 
MYSQL_USER = 'dba'
MYSQL_PASSWORD = 'ahi2021'
MYSQL_DATABASE = 'newdatabase'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)
meta = MetaData()
meta.reflect(bind=engine)
meta.tables.keys()

h1n1 = pd.read_csv('/Users/William/Desktop/H1N1_Flu_Vaccines.csv')
h1n1.to_sql('H1N1_Flu_Vaccines', con=engine, if_exists ='append') 

test = pd.read_sql('select * from newdatabase.H1N1_Flu_Vaccines', engine)
'''
Tables shows up means that it is within MySQL database
Rerun meta.reflect & meta.tables.keys() to show that it is within the database 

dict_keys(['H1N1_Flu_Vaccines', 'medicalNotesDemo'])
'''

Session = sessionmaker(bind=engine) 
session = Session() 

Base = declarative_base()
Base.metadata.create_all(engine) 

h1n1trigger = DDL("""
                  SELECT * FROM H1N1_Flu_Vaccines LIMIT 15;
                  CREATE TRIGGER H1N1_concern_trigger BEFORE INSERT ON H1N1_Flu_Vaccines
                  FOR EACH ROW BEGIN 
                  IF NEW.alert >=3 THEN
                  SIGNAL SQLSTATE '45000'
                  SET MESSAGE_TEXT = 'H1N1 concern should be a numerical value between 0 and 3. Please try again.'
                  ;END IF;
                  END;
                  """)
session.commit()
event.listen(Base.metadata, 'after_create', h1n1trigger)


