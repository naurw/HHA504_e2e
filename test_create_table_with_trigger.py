#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 23:43:24 2021

@author: William
"""

# =============================================================================
# Creating a simple table with an unidirectional trigger into production instance via MySQL for testing purposes
# - Instance can only run once; restart kernel if need be 
# - This is a TESTING template for future iterations 
# - Validation trigger works only within ORM levels; it doesn't reflect on the actual trigger list within the database
# =============================================================================
import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float 
from sqlalchemy.orm import sessionmaker, validates 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData

MYSQL_HOSTNAME = 'INSERTHERE'
MYSQL_USER = 'INSERTHERE'
MYSQL_PASSWORD = 'INSERTHERE'
MYSQL_DATABASE = 'INSERTHERE'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)
meta = MetaData()
meta.reflect(bind=engine)
meta.tables.keys()
'''
Initally outputs dict_keys([]) since there are no tables currently within this database
After running the code below, it outputs dict_keys(['medicalNotesDemo']), which is the table we had created below

print (engine.table_names()) is depreciated! 
'''

Session = sessionmaker(bind=engine) 
session = Session() 

Base = declarative_base()

class MedicalNotesDemo(Base): 
    __tablename__ = 'medicalNotesDemo'
    
    id = Column(Integer, primary_key= True) 
    name = Column(String(100))
    age = Column(Integer())
    med = Column(String(100))
    dosage = Column(Integer())
    cost = Column(Float())
    sex = Column(String(100))
    
    #Simple trigger that works for iterables
    #Not as reliable as DDL class triggers
    @validates('name')
    def validateAge(self, key, medicalNotesDemo):
        if '@' in medicalNotesDemo: 
            raise ValueError('Failed simple name validation--only letters')
        return medicalNotesDemo
            
    
Base.metadata.create_all(engine) 
# Comment this out once the data has been created

patient1 = MedicalNotesDemo(name= 'Gustaw', age= 34, med= 'Naproxen', dosage= 30, cost= 5.68, sex= 'F')
patient2 = MedicalNotesDemo(name= 'Kiyoshi', age= 16, med= 'Aspirin', dosage= 20, cost= 1.38, sex= 'M')
patient3 = MedicalNotesDemo(name= 'Ash', age= 25, med= 'Ibuprofen', dosage= 60, cost= 0.50, sex= 'M')
patient4 = MedicalNotesDemo(name= 'Bl@ke', age=4, med= 'Ibuprofen', dosage= 30, cost= 1.00, sex= 'F')
'''
Trigger successfully implemented as seen below with patient4 

ValueError: Failed simple name validation--only letters
'''

session.add(patient1)
session.add_all([patient2, patient3])
session.commit()

medicalNotesDemo = pd.read_sql('select * from newdatabase.medicalNotesDemo', engine)
medicalNotesDemo
