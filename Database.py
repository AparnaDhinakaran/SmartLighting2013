#import os

### DATABASE ###

"""
SHORTCUT (CREATES MOST RECENT DATABASE):
    Delete data.db (if you have an old database)
    Run the command
        >>> createDatabase()

REMOVING TABLES: IF YOU ALREADY HAVE AN EXISTING DATABASE:
     1) >>>drop_tables('tablename1', 'tablename2',...)
     2) >>>drop_light()
        
CREATING SOME TABLES:
    >>> create_tables('tablename')
    Shortcuts: all, alllight, artificial, cloud

CLOUD DATA:
    >>> createCloudData()

LIGHT DATA: This will input all the sensor light data. Even if you only
                dropped one light table, you can run this command. 
    >>> createLightData()

    If you would like to change the smoothing function operations,
    change the values in the function smoothing and then run:

    >>>createLightData()
    
ARTIFICIAL DATA:
    >>>create_artificial()
"""

### QUERYING FROM THE DATABASE ###

"""
Values in the Light Tables you can Request:
                unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                average REAL, daylight REAL, maxlight REAL, cluster INTEGER,
                soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,mem2 REAL,
                mem3 REAL, movingavg REAL, processed REAL

Values in the Cloud Table you can Request:
                timezone TEXT, year INTEGER, month
                INTEGER, day INTEGER, hour INTEGER, minute INTEGER,
                seconds INTEGER, unixtime REAL, cloudiness TEXT,
                cloudvalue REAL, daycloudvalue REAL

Values in the Artificial Light Tables you can Request:
                unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL, average REAL,
                cluster INTEGER

"""

import urllib2
import datetime
import numpy as np
import sqlite3
from numpy import vstack
import scipy as sp
from scipy import stats
from datetime import datetime,date
import time
from time import mktime, localtime, gmtime, strftime
import statsmodels as sm
import matplotlib as mpl
from matplotlib import pyplot as plt
import pytz
from pytz import timezone
import math
import pdb

import sqlite3
from sqlite3 import dbapi2 as sqlite3
from scipy.cluster.vq import *


##########################
### CREATE TABLE CODE ####
##########################

def drop_tables(*args):
    """This code allows any number of tables to dropped. The arguments
       are the table names written in string format and separated by a
       comma. """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    arguments = [args]
    for elem in arguments[0]:
        connection = sqlite3.connect('data.db')
        cursor.execute('DROP TABLE ' + elem)
    connection.commit()

def drop_light():
    """This shortcut code allows only the light tables to be dropped."""
    drop_tables('light1', 'light2', 'light3', 'light4', 'light5', 'light6', 'light7', 'light8', 'light9', 'light10','nasalight1', 'nasalight2', 'nasalight3', 'nasalight4', 'nasalight5', 'nasalight6', 'nasalight7', 'nasalight8', 'nasalight9', 'newnasalight1', 'newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7')


def create_tables(table = all):
    """This command creates tables in the database if they do not
        already exist. If called without any arguments, the default
        argument creates all the tables (cloud, BEST lab sensors,
        NASA sensors, and artificial tables). The other arguments
        are 'alllight', 'cloud', 'artificial'. These create a specific 
        subset of the tables. This command can also be used to create
        any particular light table. """
        
    #Create a database data.db and connect to it
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    if table == all:
        
        #Create one table for cloud measurement data

        cursor.execute('''CREATE TABLE cloud (timezone TEXT, year INTEGER, month
                        INTEGER, day INTEGER, hour INTEGER, minute INTEGER, seconds
                        INTEGER, unixtime REAL, cloudiness TEXT, cloudvalue REAL, daycloudvalue REAL,PRIMARY KEY
                        (year, month, day, hour, minute, seconds))''')

        #Create one table per artificial light level
        cursor.execute('''CREATE TABLE lighta (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightb (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightc (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightd (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        

        #Create one table per sensor for light measurement data
        cursor.execute('''CREATE TABLE light1 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light2 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
                PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light3 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light4 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                PRIMARY KEY (unixtime))''')
        
        # Light Tables for New Citrus Data (Collected Fall 2013)
        
        cursor.execute('''CREATE TABLE light5 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')
        
        cursor.execute('''CREATE TABLE light6 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')
        
        cursor.execute('''CREATE TABLE light7 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')
        
        cursor.execute('''CREATE TABLE light8 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')
        
        cursor.execute('''CREATE TABLE light9 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')
        
        cursor.execute('''CREATE TABLE light10 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        #Light tables for NASA

        cursor.execute('''CREATE TABLE nasalight1 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight2 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight3 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight4 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight5 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight6 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight7 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight8 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight9 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        # New tables for NASA light sensors (Spring 2014)

        cursor.execute('''CREATE TABLE newnasalight1 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight2 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight3 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight4 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight5 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight6 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE newnasalight7 (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL, 
                        PRIMARY KEY (unixtime))''')

    elif table == 'alllight':

        #Create one table per sensor for light measurement data
        cursor.execute('''CREATE TABLE light1 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light2 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light3 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light4 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light5 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light6 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light7 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light8 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light9 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE light10 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        #Light tables for NASA

        cursor.execute('''CREATE TABLE nasalight1 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight2 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight3 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight4 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight5 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight6 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight7 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight8 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL, cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')

        cursor.execute('''CREATE TABLE nasalight9 (unixtime REAL, weekday TEXT,
            day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
            minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
            azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
            average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
            soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
            mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
            PRIMARY KEY (unixtime))''')


    #Creates cloud table
    elif table == 'cloud':
        cursor.execute('''CREATE TABLE cloud (timezone TEXT, year INTEGER, month
                        INTEGER, day INTEGER, hour INTEGER, minute INTEGER, seconds
                        INTEGER, unixtime REAL, cloudiness TEXT, cloudvalue REAL, daycloudvalue REAL,
                        PRIMARY KEY(year, month, day, hour, minute, seconds))''')

    # Creates artificial light tables
    elif table == 'artificial':
        
        cursor.execute('''CREATE TABLE lighta (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightb (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL,cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightc (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')
        cursor.execute('''CREATE TABLE lightd (unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, x REAL, y REAL, average REAL, cluster INTEGER,
                        PRIMARY KEY (unixtime))''')

    #This will create any arbitrary light table
    else:
        cursor.execute('''CREATE TABLE ''' + table + '''(unixtime REAL, weekday TEXT,
                        day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                        minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                        azimuth REAL, cloudiness TEXT, x REAL, y REAL, exponential REAL,
                        average REAL, daylight REAL,maxlight REAL,cluster INTEGER,
                        soft1 INTEGER, soft2 INTEGER, soft3 INTEGER, mem1 REAL,
                        mem2 REAL, mem3 REAL, movingavg REAL, processed REAL,
                        PRIMARY KEY (unixtime))''')
        

    #Save your changes
    connection.commit()

##################
### CLOUD DATA ###
##################

cloudiness=['Clear','Partly','Scattered','Light','Mostly','Rain','Overcast','Heavy','Fog','Haze']
values=[0,2,4,4,7,7,8,8,4,4]
clouddict = {'Clear': 0, 'Partly Cloudy':2, 'Scattered Clouds':4, 'Light Rain':4, 'Mostly Cloudy':7, 'Rain':7, 'Overcast':8, 'Heavy Rain':8, 'Fog':4, 'Haze':4}


def cloud_make_unix_timestamp(date_string, time_string):
    """This command converts string format of date into unix timstamps."""
    format = '%Y %m %d %H %M %S'
    return time.mktime(time.strptime(date_string + " " + time_string, format))
                       
    
def isLeapYear( year):
    """This command checks if a year is a leap year."""
    if (year % 400 == 0) :
        return True
    if (year % 100 == 0) :
        return False
    if (year % 4 == 0):
        return True
    else:
        return False              
  

def daysInMonth(month,year):
    """This command determines the number of days in a month"""
    if (month == 2):
      if (isLeapYear(year)):
          return 29;
      else:
          return 28
    elif (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
      return 31
    else :
      return 30
 
def dayInYear(month, day, year):
    """This command determines what day of the year that particular day is."""
    current = 1
    numberOfDays = day
    while (current < month):
        numberOfDays = numberOfDays + daysInMonth(current, year)
        current = current + 1
    return numberOfDays

def difference(month1, day1, year1, month2, day2, year2):
    """This code determines the difference in the number of days between the two days.
        Month1, day1, and year1 are later days than month2, day2, and year2"""
    daycounter = 0;  
    if (year1 == year2):
        return (dayInYear(month1, day1, year1) - dayInYear(month2, day2,year2))
    elif (isLeapYear(year2)):
        daycounter = daycounter + (366 - dayInYear(month2, day2, year2))
    else:
        daycounter = daycounter + (365 - dayInYear(month2, day2, year2))
    daycounter = daycounter + dayInYear(month1, day1, year1)
    current = year2 + 1
    while (current < year1):
        if (isLeapYear(current)):
            daycounter = daycounter + 366
            current = current + 1
        else:
            daycounter = daycounter + 365
            current = current + 1
    return daycounter


def arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2):
    """This code returns the days and months and years in between 2
        different days. It returns them in three different arrays so
        that printing all the days in between 2 days is possible. """
    daysleftinmonth2 = daysInMonth(month2, year2) - day2 + 1
    if year1 == year2:
            if month1 == month2:
                monthsinbetween = 0
            else:
              monthsinbetween= month1 - month2 - 1
    else:
        monthsleftinyear2 = 12 - month2 - 1
        monthsinbetween = monthsleftinyear2 + (12 *(year1 - (year2+1))) + month1
    dayarray = []
    montharray = []
    yeararray= []
    if year1 == year2:
        if month2 == month1:
          currentdays = day1 - day2 + 1
        else:
            currentdays = daysleftinmonth2
    else:
        currentdays = daysleftinmonth2        
    currentday = day2
    currentmonth = month2
    currentyear = year2
    while currentdays > 0:
        dayarray.append(currentday)
        montharray.append(currentmonth)
        yeararray.append(currentyear)
        currentdays = currentdays - 1
        currentday = currentday + 1
    fullmonths = monthsinbetween
    currentmonth = month2 + 1
    while fullmonths > 0:
        if currentmonth > 12:
              currentmonth = 1
              currentyear = currentyear + 1
        daystoadd = daysInMonth(currentmonth, currentyear)
        currentdaytoadd = 1
        while daystoadd > 0:
            dayarray.append(currentdaytoadd)
            montharray.append(currentmonth)
            yeararray.append(currentyear)
            currentdaytoadd = currentdaytoadd + 1
            daystoadd = daystoadd - 1
        currentmonth = currentmonth + 1
        fullmonths = fullmonths - 1
    daysinday1 = day1
    finaldaytoadd = 1
    if month2 != month1 or year1 != year2:
          while daysinday1 > 0:
              dayarray.append(finaldaytoadd)
              montharray.append(month1)
              yeararray.append(year1)
              finaldaytoadd = finaldaytoadd + 1
              daysinday1 = daysinday1 - 1
    return [dayarray, montharray, yeararray]

def arrayofdays(month1,day1,year1,month2,day2,year2):
    """This code returns just the days between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[0]

def arrayofmonths(month1,day1,year1,month2,day2,year2):
    """This code returns just the months between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[1]

def arrayofyears(month1,day1,year1,month2,day2,year2):
    """This code returns just the years between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[2]

def day_cloudiness():
    """This code determines what the average cloudiness of a day is
        and updates the database to this daily cloudiness value. This value
        can be extracted from the database with the tag daycloudvalue."""
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    x = cursor.execute('SELECT unixtime from cloud')
    cloudtimes = []
    for i in x.fetchall():
        cloudtimes.append(i[0])
    for elem in cloudtimes:
        #elem = cloudtimes[0]
        day = (cursor.execute('SELECT day FROM cloud WHERE unixtime = ' + str(elem))).fetchall()[0][0]
        month = (cursor.execute('SELECT month FROM cloud WHERE unixtime = ' + str(elem))).fetchall()[0][0]
        year = (cursor.execute('SELECT year FROM cloud WHERE unixtime = ' + str(elem))).fetchall()[0][0]
        values = (cursor.execute('SELECT cloudvalue FROM cloud WHERE day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = ' + str(year))).fetchall()
        total = 0;
        checker = False
        i = 0
        while i < len(values):
            if values[i][0] != float('nan') and values[i][0] != None:
                checker = True
                total = total + values[i][0]
            i = i + 1
        if checker:
            average = total/len(values)
        else:
            average = 'nan'
        cursor.execute('UPDATE cloud SET daycloudvalue = ? WHERE unixtime = ? ', (average, elem))
    connection.commit()
      

def createCloudData(end = strftime('%Y %m %d', time.localtime()), start = "2012 05 01", feature = "history", station = "KOAK"):
    """Adds all the wunderground data to the cloud data starting from start
    date START until end date END. You can specify the feature FEATURE to pull
    either historical data or hourly data. You also must specify the weather
    station STATION. Default values are above."""
    #Connect to the database data.db
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    start_split = start.split()
    end_split = end.split()
    startyear = int(start_split[0])
    endyear = int(end_split[0])
    startmonth = int(start_split[1])
    endmonth = int(end_split[1])
    startday = int(start_split[2])
    endday = int(end_split[2])

    DD = arrayofdays(endmonth,endday,endyear,startmonth,startday,startyear)
    MM = arrayofmonths(endmonth,endday,endyear,startmonth,startday,startyear)
    YYYY = arrayofyears(endmonth,endday,endyear,startmonth,startday,startyear)
    
    for i in range(len(DD)):
        month = str(MM[i])
        day = str(DD[i])
        if (DD[i] < 10):
            day = "0" + day
        if (MM[i] < 10):
            month = "0" + month
        YYYYMMDD=str(YYYY[i])+month+day
        features=feature+"_"+YYYYMMDD
        url="http://api.wunderground.com/api/46c535271ddf6901/"+features+"/q/"+station+".json"
        print(url)
        data=urllib2.urlopen(url).read()
        getdata=data.split(",")
        for count in range(len(getdata)):
            if '"tzname":' in getdata[count]:
                if '"tzname": "UTC"' not in getdata[count]:
                    minute = getdata[count-1].split(":")
                    y2 = minute[1].strip().replace("\"","")
                    if (y2 == "53"):
                        timezone = getdata[count].split(":")
                        x = timezone[1].replace("\"","").replace("}","").strip()
                        hour = getdata[count-2].split(":")
                        y1 = hour[1].strip().replace("\"","")
                        clouds = getdata[count+30].split(":")
                        cloudiness = clouds[1].replace("\"","")
                        if cloudiness in clouddict.keys(): 
                            cloudvalue = clouddict[cloudiness]
                        else:
                            cloudvalue = float('nan')
                        unixtime = cloud_make_unix_timestamp(str(YYYY[i]) + " " + month + " " + day, y1 + " " + y2 + " " + "00")
                        to_db = [x, YYYY[i], MM[i], DD[i], int(y1), int(y2), 0, unixtime, cloudiness,cloudvalue, float('nan')]
                        cursor.execute('INSERT OR IGNORE INTO cloud VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                               to_db)
        
    #Save your changes
    connection.commit()
    day_cloudiness()
    

def updateCloudData():
    """This command updates the cloud value in the database"""
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT year, month, day, MAX(unixtime) FROM cloud')
    #cursor.execute('SELECT MAX(unixtime) FROM cloud')
    current = cursor.fetchall()[0]
    #for i in cursor.fetchmany(2):
     #   print i
    #print(current)
    year = str(current[0])
    month = str(current[1])
    day = str(current[2])
    if month < 10:
          month = "0" + month
    if day < 10:
          day = "0" + day
    start = year + " " + month + " " + day
    ttb = time.localtime()
    end = strftime("%Y %m %d", ttb)
    #print(start)
    #print(end)
    createCloudData(end, start)


######################################        
### LIGHT TABLES CODE ################
######################################

#lat and lon global variables of BEST lab
best_lat = "37 52 27.447"
best_lon = "122 15 33.3864 W"
best_timezone = "US/Pacific"

#lat and lon global variables for NASA
nasa_lat = "37 24 54.7194"
nasa_lon = "122 2 53.8794 W"
nasa_timezone = "US/Pacific"

def change_loc(sens_no, nasa, new):
    """Changes the value of SENS_NO in the sensors_loc dictionary to the
    tuple NEW."""
    if nasa:
        nasa_sensors_loc[sens_no] = new
    else:
        sensors_loc[sens_no] = new

#Dictionary that maps each BEST lab sensor number to its location (x, y)
sensors_loc = {1:(0,0), 2:(0,1), 3:(1,0), 4:(1,1), '1old':(1,2), '2old':(2,1),
               '3old':(2,0), '4old':(0,2), 'a': (3,1), 'b': (4,2), 'c': (5,2), 'd':
               (9,0)}

#Dictionary that maps each NASA lab sensor number to its location (x, y)
nasa_sensors_loc = {1:(0,0), 2:(0,1), 3:(1,0), 4:(1,1), 5:(1,2), 6:(2,1),
                    7:(3,3), 8:(4,3), 9:(5,5)}

#Dictionary that maps each BEST lab sensor number to its sensor ID.
sensors_dict = {1:"7140b2da-94cd-5bae-a1e8-cb85a6715bf5",
                2:"f862a13d-91ee-5696-b2b1-b97d81a47b5b",
                3:"b92ddaee-48de-5f37-82ed-fe1f0922b0e5",
                4:"8bb0b6a2-971f-54dc-9e19-14424b9a1764",
                '1old':'27cfdd4e-c0dd-5ba8-85fd-5b4f063f872f',
                '2old':'310eea9e-8634-54b6-bd5e-8d711e86531d',
                '3old':'46e7060b-a5c8-58b7-8708-4ecaddbafb6b',
                '4old':'f71e64e5-b27c-51b2-8ac4-f56db13aa059'}

#Dictionary that maps each NASA lab sensor number to its sensor ID.
nasa_sensors_dict = {1:"6325ce7e-5afe-5301-bf11-391f10703998",
                     2:"473da30c-691f-532b-813d-10db0f9adc34",
                     3:"e82ad906-4fbf-5747-beff-72d0c5efccba",
                     4:"7a66bf12-4265-5139-9251-f33d12b93298",
                     5:"7e69270c-305b-5f1c-9dc5-995d594f2a34",
                     6:"06d693f6-1f6e-5746-ba99-ac49383b0a21",
                     7:"2ae4fa93-0f64-52b8-bd64-49c6850ee474",
                     8:"095c683c-ff7e-55f0-8266-8ba2d0320ed4",
                     9:"67ce294e-c10c-5024-b8ea-d0288bcd8d69"}

def parse(url):
    """Returns a list of the timestamps, readings, and unixtimes of each
    entry from the raw data provided by the input url."""
    timestamp=[]
    reading=[]
    timest=[]
    temp=[]
    unixtime=[]
    webpage = urllib2.urlopen(url).read()
    page = str.split(webpage, '[')
    for count in range(len(page)):
        z1=str.split(page[count],',')
        temp.append(z1)
        count+=1
    getvar = temp[3:]
    for count in range(len(getvar)):
        t=float(getvar[count][0])/1000
        unixtime.append(float(getvar[count][0]))
        ttb=time.localtime(t)
        #Returns time in string format: "Wed 21 11 2012 16 45 53"
        tim=strftime("%a %d %m %Y %H %M %S",ttb)
        #For debugging:
        if (count == 0):
            print(tim)
        timestamp.append(tim.split())
        read=str.split((getvar[count][1]),']')
        reading.append(float(read[0]))
        #For debugging:
        if (count == 0):
            print(float(read[0])) #37.851485925
        count+=1
    return [timestamp, reading, unixtime]

def getSunpos(lat, lon, timezon, year, month, day, hour, minute, seconds):
    """Returns a list containing the altitude and the azimuth given the
    latitude LAT, longitude LON, timezone TIMEZON, year YEAR, month MONTH,
    minute MINUTE, and seconds SECONDS."""
    splat = str.split(lat)
    splon = str.split(lon)
    latitude = float(splat[0]) + float(splat[1])/60 + float(splat[2])/3600
    if splon[3] == 'W':
        longitude = -(float(splon[0]) + float(splon[1])/60 +
                      float(splon[2])/3600)
    else:
        longitude = float(splon[0]) + float(splon[1])/60 +\
        float(splon[2])/3600
    local = pytz.timezone(timezon)
    loctime = str(year) + '-' + str(month) + '-' + str(day) + ' ' +\
                str(hour) + ':' + str(minute) + ':' + str(seconds)
    naive = datetime.strptime(loctime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt.strftime("%Y-%m-%d %H:%M:%S")
    utcsplit = str.split(str(utc_dt))
    utcdt = str.split(utcsplit[0],'-')
    utctime = str.split(utcsplit[1],'+')
    utctimefinal = str.split(utctime[0],':')
    year = utcdt[0]
    month = utcdt[1]
    day = utcdt[2]
    hour = utctimefinal[0]
    minute = utctimefinal[1]
    second = utctimefinal[2]
    #+1 for e and -1 for w for dst
    houronly = float(hour) + float(minute)/60 + float(second)/3600
    delta = int(year)-1949
    leap = int(delta/4)
    doy = [31,28,31,30,31,30,31,31,30,31,30,31]
    if int(year)%4 == 0:
        doy[1] = 29
    dayofyear = sum(doy[0:(int(month)-1)]) + int(day)
    jd = 2432916.5 + delta*365 + dayofyear + leap + houronly/24
    actime = jd - 2451545
    pi = 3.1415926535897931
    rad = pi/180
    
    #mean longitude in degrees between 0 and 360
    L = (280.46 + 0.9856474*actime)%360
    if L < 0:
        L+=360
    #mean anomaly in radians
    g = (357.528 + 0.9856003*actime) % 360
    if g < 0:
        g+=360
    g = g*rad
    #ecliptic longitude in radians
    eclong = (L + 1.915*math.sin(g) + 0.02*math.sin(2*g)) % 360
    if eclong < 0:
        eclong+=360
    eclong = eclong*rad
    #ecliptic obliquity in radians
    ep = (23.439 - 0.0000004*actime)*rad
    #get right ascension in radians between 0 and 2 pi
    num = math.cos(ep)*math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan(num/den)
    if den < 0:
        ra+=pi
    elif den > 0 and num < 0:
        ra+=2*pi
    #get declination in radians
    dec = math.asin(math.sin(ep)*math.sin(eclong))
    #get greenwich mean sidereal time
    gmst = (6.697375 + 0.0657098242*actime + houronly) % 24
    if gmst < 0:
        gmst+=24
    #get local mean sidereal time in radians
    lmst=(gmst + longitude/15) % 24
    if lmst < 0:
        lmst+=24
    lmst = lmst*15*rad
    #get hour angle in radians between -pi and pi
    ha = lmst - ra
    if ha < -pi:
        ha+=2*pi
    elif ha > pi:
        ha = ha - 2*pi
    #change latitude to radians
    latrad = latitude*rad
    #calculate elevation and azimuth in degrees
    el=math.asin(math.sin(dec)*math.sin(latrad) +
                 math.cos(dec)*math.cos(latrad)*math.cos(ha))
    az=math.asin(-math.cos(dec)*math.sin(ha)/math.cos(el*rad))
    #approximation for azimuth
    #if az==90, elcrit=math.degrees(math.asin(math.sin(dec)/math.sin(latitude)))
    if math.sin(dec) - math.sin(el)/math.sin(latrad) >= 0 and\
        math.sin(az) < 0:
        az+=2*pi
    elif math.sin(dec) - math.sin(el)/math.sin(latrad) < 0:
        az = pi-az
    eldeg = round(math.degrees(el),2)
    azdeg = round(math.degrees(az),2)
    if eldeg > -0.56:
        refrac = 3.51561*(0.1594 + 0.0196*eldeg + 0.00002*math.pow(eldeg,2))\
                    /(1 + 0.505*eldeg + 0.0845*math.pow(eldeg,2))
    else:
        refrac = 0.56
    eldeg=eldeg+refrac
    #print eldeg,azdeg
    #data is saved for future reference
    return [str(eldeg), str(azdeg)]


def createData(sens_no, old, nasa, start, end, lat, lon, timezon):
    """This function adds data for BEST lab sensor SENS_NO into its
    respective light table starting from unix timestamp (in milliseconds)
    START and ending at unix timestamp (in milliseconds) END. It generates
    sunposition data using the given LAT, LON, and TIMEZON. If these are
    not specified, createData resorts to the default LAT, LON, and TIMEZON
    values, which are the values for the BEST Lab in Berkeley, CA. LAT
    format is "degrees minutes seconds" (north is positive). LON format is
    "degrees minutes seconds W|E" (W for west and E for east). TIMEZON
    choices can be looked up. Must be compatible with python utc timezones.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    if old:
        sensorID = sensors_dict[str(sens_no)+'old']
        sensorLoc = sensors_loc[str(sens_no) + 'old']
        table = "light" + str(sens_no)
    elif nasa:
        sensorID = nasa_sensors_dict[sens_no]
        sensorLoc = nasa_sensors_loc[sens_no]
        table = "nasalight" + str(sens_no)
    else:
        sensorID = sensors_dict[sens_no]
        sensorLoc = sensors_loc[sens_no]
        table = "light" + str(sens_no)
    x = sensorLoc[0]
    y = sensorLoc[1]
    url = "http://new.openbms.org/backend/api/prev/uuid/" + sensorID +\
          "?&start=" + start + "&end=" + end + "&limit=100000&"
    timestamp, reading, unixtime = parse(url)
    for count in range(len(reading)):
        time = timestamp[count]
        sunpos = getSunpos(lat, lon, timezon, time[3], time[2],
                           time[1], time[4], time[5], time[6])
        cloud = cursor.execute('SELECT cloudiness FROM cloud WHERE day = ' +
                               str(time[1]) + ' AND month = ' + str(time[2]) +
                               ' AND year = ' + str(time[3]) + ' AND hour = ' +
                               str(time[4]))
        cloudiness = cloud.fetchone()
        if cloudiness is not None:
            to_db = [unixtime[count], time[0], time[1], time[2], time[3],
                     time[4], time[5],time[6], reading[count], sunpos[0],
                     sunpos[1], str(cloudiness[0]), x, y, float('NaN'),
                     float('NaN'), float('NaN'), float('NaN'), float('Nan'),
                     float('NaN'), float('NaN'), float('NaN'), float('Nan'),
                     float('NaN'), float('NaN'), float('NaN'), float('Nan')]
        else:
            to_db = [unixtime[count], time[0], time[1], time[2], time[3],
                     time[4], time[5],time[6], reading[count], sunpos[0],
                     sunpos[1], "None", x, y, float('NaN'), float('NaN'),
                     float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                     float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                     float('NaN'), float('NaN'), float('Nan')]
        cursor.execute('INSERT OR IGNORE INTO ' + table +
                       ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       to_db)      
    connection.commit()

def createNewCitris(lat, lon, timezon):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    lines = []
    with open("./COMPILED_test_data_8_30_to_10_23.txt") as file:
    #with open("./newdata.txt") as file:
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            lines.append(line.rstrip().split(","))
            print line.rstrip().split(",")
    lists = []
    for line in lines:
        lists.append([line[0].split()])

    date,time,lux,sensor = "","","",""


    for elem in lists:
        if len(elem[0]) == 12:
            date = (str(elem[0][0])).split("-")
            tim = str(elem[0][1]).split(":")
            date_string = date[0] + " " + date[1] + " " + date[2]
            time_string = (str(tim[0]) + " " + str(tim[1]) + " " + "00")
            unix = int(cloud_make_unix_timestamp(date_string, time_string)) * 1000
            lux = str(elem[0][7])
            sensor = str(int(elem[0][9]))
            print "sensor num: ", sensor
            table = 'light' + sensor
            #table = 'nasalight' + sensor
            #sunpos = getSunpos(lat, lon, timezon, date[0], date[1], date[2], tim[0], tim[1], 0)
            sunpos = getSunpos(lat, lon, timezon, date[0], date[1], date[2], tim[0], tim[1], 0)
            to_db = [unix, "Unknown", date[2], date[1], date[0],
                         tim[0], tim[1],0, lux, sunpos[0],
                         sunpos[1], "None", float('Nan'), float('NaN'), float('NaN'), float('NaN'),
                         float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                         float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                         float('NaN'), float('NaN'), float('Nan')]
            print "to_db: ", to_db
            cursor.execute('INSERT OR IGNORE INTO ' + table +
                           ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           to_db)
    connection.commit()

def createNewNasa(lat, lon, timezon):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    lines = []
    #with open("./COMPILED_test_data_8_30_to_10_23.txt") as file:
    with open("./newnasadata.txt") as file:
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            lines.append(line.rstrip().split(","))
            print line.rstrip().split(",")
    lists = []
    for line in lines:
        lists.append([line[0].split()])

    date,time,lux,sensor = "","","",""


    for elem in lists:
        if len(elem[0]) == 12:
            date = (str(elem[0][0])).split("-")
            tim = str(elem[0][1]).split(":")
            date_string = date[0] + " " + date[1] + " " + date[2]
            time_string = (str(tim[0]) + " " + str(tim[1]) + " " + "00")
            unix = int(cloud_make_unix_timestamp(date_string, time_string)) * 1000
            lux = str(elem[0][7])
            sensor = str(int(elem[0][9]))# + 4)
            print "sensor num: ", sensor
            #table = 'light' + sensor
            table = 'newnasalight' + sensor
            #sunpos = getSunpos(lat, lon, timezon, date[0], date[1], date[2], tim[0], tim[1], 0)
            sunpos = getSunpos(lat, lon, timezon, date[0], date[1], date[2], tim[0], tim[1], 0)
            to_db = [unix, "Unknown", date[2], date[1], date[0],
                         tim[0], tim[1],0, lux, sunpos[0],
                         sunpos[1], "None", float('Nan'), float('NaN'), float('NaN'), float('NaN'),
                         float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                         float('NaN'), float('NaN'), float('Nan'),float('NaN'),
                         float('NaN'), float('NaN'), float('Nan')]
            print "to_db: ", to_db
            cursor.execute('INSERT OR IGNORE INTO ' + table +
                           ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           to_db)
    connection.commit()
    
def createRawLightData():
    """Adds all the data starting from the beginning of data collection
    until the current time for BEST lab sensors 2, 3, and 4 and Nasa ."""
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    #Older Data
    createData(1, True,False,"1355616600000","1359446399000",best_lat, best_lon, best_timezone)
    createData(2, True, False,"1355616600000","1359446399000",best_lat, best_lon, best_timezone)
    createData(3, True,False,"1355616600000","1359446399000",best_lat, best_lon, best_timezone)
    createData(4, True,False,"1355616600000","1359446399000",best_lat, best_lon, best_timezone)

    #Current Data

    createData(1, False,False, "1347059530000", str(int(time.time())*1000),
               best_lat, best_lon, best_timezone)
    createData(2,False, False, "1349478489000", str(int(time.time())*1000),
               best_lat, best_lon, best_timezone)
    createData(3,False, False, "1353545153000", str(int(time.time())*1000),
               best_lat, best_lon, best_timezone)
    createData(4,False, False, "1353545237000", str(int(time.time())*1000),
               best_lat, best_lon, best_timezone)
    createData(1, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(2, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(3, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(4, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(5, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(6, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(7, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(8, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    createData(9, False,True, "1335859200000", str(int(time.time())*1000), nasa_lat,
               nasa_lon, nasa_timezone)
    
    #Recent New Data
    createNewCitris(best_lat, best_lon, best_timezone)
    createNewNasa(nasa_lat, nasa_lon,nasa_timezone)
    connection.commit()
    

def createLightData():
    """This command calls many other functions to fill in all
        the lighttables. It primarily creates the light data and
        then smoothes the values in a separate column. Then it
        deletes rows from the database that have light values
        greater than 12000 as they are outliers. Then it clusters
        the data within light1 and light8 and places those values
        into the other corresponding sensor tables. """
    print "Fetching Raw Light Data"
    createRawLightData()
    print "Deleting Extreme Lights"
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM light1 WHERE light > 12000')
    cursor.execute('DELETE FROM light2 WHERE light > 12000')
    cursor.execute('DELETE FROM light3 WHERE light > 12000')
    cursor.execute('DELETE FROM light4 WHERE light > 12000')
    cursor.execute('DELETE FROM light5 WHERE light > 12000')
    cursor.execute('DELETE FROM light6 WHERE light > 12000')
    cursor.execute('DELETE FROM light7 WHERE light > 12000')
    cursor.execute('DELETE FROM light8 WHERE light > 12000')
    cursor.execute('DELETE FROM light9 WHERE light > 12000')
    cursor.execute('DELETE FROM light10 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight1 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight2 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight3 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight4 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight5 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight6 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight7 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight8 WHERE light > 12000')
    cursor.execute('DELETE FROM nasalight9 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight1 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight2 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight3 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight4 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight5 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight6 WHERE light > 12000')
    cursor.execute('DELETE FROM newnasalight7 WHERE light > 12000')
    connection.commit()
    print "Processing Light Tables"
    insert_movingavg()
    insert_processed_light()
    print 'Smoothing Light Tables'
    smoothingtables()
    # TODO: need to cluster new nasa light tables --> need the window sensor!
    print " Hard Clustering Light Tables"
    light1 = cluster('light1', 1354348800000, 1364799600000)
    nasalight8 = cluster('nasalight8', 1335859200000, 1358357465000)
    light8 = cluster('light8', 1377887460000, 1382563860000)
    create_cluster('light1', 1354348800000, 1364799600000, light1)
    create_cluster('nasalight8', 1335859200000, 1358357465000, nasalight8)
    create_cluster('light8', 1377887460000, 1382563860000, light8)
    print "Updating Other Clusters"
    update_clusters('light1')
    update_clusters('nasalight8')
    update_clusters('light8')
#    print "Soft-Clustering NASA"
#    soft_cluster('NASA')
#    print "Soft-Clustering Hesse"
#    soft_cluster('Hesse')
#    print "Soft-Clustering NewCitris"
#    soft_cluster('NewCitris')
#    print "Soft-Clustering NewNasa"
#    soft_cluster('NewNasa')
#    
"""
    Note: This part of the code has been commented out because it takes a long time.
    To fill these columns in the database, remove the red hashtags. 
    """

    #max_light(1, False)
    #max_light(2, False)
    #max_light(3, False)
    #max_light(4, False)

    #print("Averaging light1")
    #average_light(1, False)
    #print("Averaging light2")
    #average_light(2, False)
    #print("Averaging light3")
    #average_light(3, False)
    #print("Averaging light4")
    #average_light(4, False)


# Include Maximum Light Level in Database
def max_light(sensor, nasa):
    if nasa:
        table = 'nasalight' + str(sensor)
    else:
        table = 'light' + str(sensor)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for month in range(9,13):
        for day in range(1,32):
            x = cursor.execute('SELECT MAX(light) FROM ' + table + ' WHERE day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = 2012')
            maxlight = x.fetchall()[0][0]
            cursor.execute('UPDATE ' + table + ' SET maxlight = ? WHERE day = ? AND month = ? and year = 2012 ', (maxlight, day, month))
    print('Done with 2012')
    connection.commit()    
    for month in range(1,7):
        for day in range(1,32):
            x = cursor.execute('SELECT MAX(light) FROM ' + table + ' WHERE day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = 2012')
            maxlight = x.fetchall()[0][0]
            cursor.execute('UPDATE ' + table + ' SET maxlight = ? WHERE day = ? AND month = ? and year = 2012 ', (maxlight, day, month))
    print('Done with 2013')
    connection.commit()


#Include Average Light Level in Database

def average_light(sensor, nasa):
    if nasa:
        table = 'nasalight' + str(sensor)
    else:
        table = 'light' + str(sensor)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for month in range(9,13):
        for day in range(1,32):
            x = cursor.execute('SELECT AVG(light) FROM ' + table + ' WHERE altitude > -5 AND day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = 2012')
            average =  x.fetchall()[0][0]
            cursor.execute('UPDATE ' + table + ' SET daylight = ? WHERE day = ? AND month = ? and year = 2012 ', (average, day, month))
            connection.commit()
    for month in range(1,7):
        for day in range(1,32):
            x = cursor.execute('SELECT AVG(light) FROM ' + table + ' WHERE altitude > -5 AND day = ' + str(day) + ' AND month = ' + str(month) + ' AND year = 2013')
            average =  x.fetchall()[0][0]
            cursor.execute('UPDATE ' + table + ' SET daylight = ? WHERE day = ? AND month = ? and year = 2013 ', (average, day, month))
            connection.commit()
            
def updateLightData():
    """Updates all the data in BEST lab sensors 2, 3, and 4 by calling
    updateData on each sensor."""
    updateData(1, False,False, best_lat, best_lon, best_timezone)
    updateData(2, False,False, best_lat, best_lon, best_timezone)
    updateData(3, False,False, best_lat, best_lon, best_timezone)
    updateData(4, False,False, best_lat, best_lon, best_timezone)
    updateData(1, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(2, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(3, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(4, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(5, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(6, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(7, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(8, False,True, nasa_lat, nasa_lon, nasa_timezone)
    updateData(9, False,True, nasa_lat, nasa_lon, nasa_timezone)

def updateData(sens_no, old, nasa, lat, lon, timezon):
    """Updates all the data starting from the time of the latest entry of
    each time table until the current time for BEST lab sensor number
    SENS_NO. It generates sunposition data using the given LAT, LON, and
    TIMEZON. If these are not specified, createData resorts to the default
    LAT, LON, and TIMEZON values, which are the values for the BEST Lab
    in Berkeley, CA. LAT format is "degrees minutes seconds" (north is
    positive). LON format is "degrees minutes seconds W|E" (W for west and
    E for east). TIMEZON choices can be looked up. Must be compatible with
    python utc timezones.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    if nasa:
        sensorID = nasa_sensors_dict[sens_no]
        sensorLoc = nasa_sensors_loc[sens_no]
        table = "nasalight" + str(sens_no)
    else:
        sensorID = sensors_dict[sens_no]
        sensorLoc = sensors_loc[sens_no]
        table = "light" + str(sens_no)
    x = sensorLoc[0]
    y = sensorLoc[1]
    cursor.execute('SELECT MAX(unixtime) FROM ' + table)
    start = int(cursor.fetchone()[0])
    end = int(time.time())*1000
    limit = (end - start)/300000
    start = str(start)
    end = str(end)
    print("limit is:" + str(limit))
    print("Start is:" + str(start))
    print("End is:" + str(end))
    createData(sens_no, old, nasa, start, end,lat, lon, timezon)
    #Save your changes
    connection.commit()




#############################
### PROCESSING LIGHT CODE ###
#############################

def movavg(testbed = 'all',mote = 'all',movavg_len=6):
    
    #determine options
    allmotes = [ ['nasalight1','nasalight2','nasalight3','nasalight4','nasalight5','nasalight6','nasalight7','nasalight8','nasalight9'],['light1','light2','light3','light4','light5', 'light6', 'light7', 'light8', 'light9', 'light10'], ['newnasalight1', 'newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7'] ]
    if testbed == 'all' and mote == 'all':
        tb = ['NASA','Hesse', 'NewNasa']
        motes = allmotes
    elif testbed != 'all':
        tb = [testbed]
        if testbed == 'NASA' and mote == 'all':
            motes = [ allmotes[0] ]
        elif testbed == 'Hesse' and mote == 'all':
            motes = [ allmotes[1] ]
        elif testbed == 'NewNasa' and mote == 'all':
            motes = [ allmotes[2] ]
        else:
            motes = [ [mote] ]
    else:
        print "Option Error: Mote must be 'all' if Testbed is 'all'!"
    motelist = []
    for count in range(len(motes)):
        motelist = motelist+motes[count]

    #connect db
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()

    #initialize
    movavg = dict()
    unixtimes = dict()

    #retrieve unixtimes (to process all raw data)
    for mote in motelist:
        cursor.execute('SELECT MIN(unixtime),MAX(unixtime) FROM '+str(mote))
        unixtimedata = cursor.fetchall()
        unixtimerange = list(unixtimedata[0])
        unixtimes[mote] = unixtimerange

        #determine the moving average using movavg_len
        cursor.execute('SELECT light,unixtime FROM '+str(mote)+' WHERE unixtime>= '+str(unixtimerange[0])+' AND unixtime<= '+str(unixtimerange[1]))        
        alldata = cursor.fetchall()
        movavg[mote] = []
        total = 0
        for count in range(len(alldata)):
            if count < movavg_len:
                total = total + alldata[count][0]
            else:
                total = total + alldata[count][0] - alldata[count-movavg_len][0]
            movavg[mote].append([total/movavg_len,alldata[count][1]])

    return movavg

def insert_movingavg():
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    moving_avg = movavg()  
    light_tables = ['light1', 'light2', 'light3', 'light4','light5', 'light6', 'light7', 'light8', 'light9', 'light10','nasalight1', 'nasalight2', 'nasalight3','nasalight4', 'nasalight5', 'nasalight6', 'nasalight7', 'nasalight8', 'nasalight9', 'newnasalight1', 'newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7']
    for table in light_tables:
        data = moving_avg[table]
        for elem in data:
            avg = elem[0]
            unix = elem[1]
            cursor.execute('UPDATE ' + str(table) + ' SET movingavg = ' + str(avg) + ' WHERE unixtime = ' + str(unix))
        connection.commit()

def insert_processed_light(avg_len=3):
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    light_tables = ['light1', 'light2', 'light3', 'light4','light5', 'light6', 'light7', 'light8', 'light9', 'light10','nasalight1', 'nasalight2', 'nasalight3','nasalight4', 'nasalight5', 'nasalight6', 'nasalight7', 'nasalight8', 'nasalight9', 'newnasalight1', 'newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7']
    for table in light_tables:

        #get threshold time
        cursor.execute('SELECT MIN(unixtime) FROM '+str(table))
        threshold = cursor.fetchall()[0][0]

        #processing
        print 'processing '+str(table)
        cursor.execute('SELECT light, movingavg, unixtime, cluster FROM ' + str(table))
        data = cursor.fetchall()
        i = 1
        while i < len(data):
            if i == len(data)/4:
                print '25%'
            elif i == len(data)/2:
                print '50%'
            elif i == 3*len(data)/4:
                print '75%'
            elif i%5000 == 0:
                print i,' ',len(data)
            current_light = data[i][0]
            previous_light = data[i-1][0]
            value = abs(current_light - previous_light)
            other = abs(data[i][1] - previous_light) * 2.0
            if value > other:

                #retrieve closest avg_len number of data to current
                clust = data[i][3]
                unix = data[i][2]
                replace = []
                retrieved = 'not done'
                while retrieved == 'not done': #a loop is a day
                    if clust != None:
                        cursor.execute('SELECT light,MAX(unixtime) FROM '+str(table)+' WHERE cluster = '+str(clust)+' AND unixtime < '+str(unix)+' AND unixtime >= '+str(unix-86400000))
                    else:
                        cursor.execute('SELECT light,MAX(unixtime) FROM '+str(table)+' WHERE unixtime< '+str(unix)+' AND unixtime >= '+str(unix-86400000))
                    datum = cursor.fetchall()
                    if datum[0][0] >= 0:
                        replace.append(datum[0][0])
                    unix-=86400000
                    if unix < threshold or abs(data[i][2]-unix) >= 86400000*14:
                        replace = replace + [current_light for n in range(avg_len-len(replace))] 
                        retrieved = 'done'
                    if len(replace) == avg_len:
                        retrieved = 'done'

                #average
                replace = sum(replace)/avg_len
                
                cursor.execute('UPDATE ' + str(table) + ' SET processed = ' + str(replace) + ' WHERE unixtime = ' + str(data[i][2]))
                i+=1
            else:
                cursor.execute('UPDATE ' + str(table) + ' SET processed = ' + str(current_light) + ' WHERE unixtime = ' + str(data[i][2]))
                i+=1
        cursor.execute('UPDATE ' + str(table) + ' SET processed = ' + str(data[0][0]) + ' WHERE unixtime = ' + str(data[0][2]))
        connection.commit()


#######################
### SMOOTHING CODE ###
#######################

def smoothing(moteNum, testbed, smoothtype, movingStatsWindow=8, expWindow=12, Alpha=0.7):
    """This function is an exterior function that smoothes the light values.
    The arguments to this function can be changed here and then when createLightData()
    runs, it will update the smoothing table values with the new smoothing values.
    moteNum is the sensor number and nasa is a true or false argument for whether it
    is nasa sensors or BEST Lab sensors. The smoothtype asks for exponential or average
    type of smoothing. The remaining arguments are particular types of smoothing values that
    Jacob Richards saw fit. """
    #define arrays
    data1=[]
    time1=[]
    hour1=[]
    ROC1=[]
    RROC1=[]
    mean1=[]
    stdev1=[]
    esmooth1=[]
    output=[]
    nROC1=[]
    nRROC1=[]

    sensornumber = moteNum
    #get data
    if testbed == 'NASA':
        sensor='nasalight'+str(sensornumber)
    elif testbed == 'NewNasa':
        sensor='newnasalight'+str(sensornumber)
    else:
        sensor='light'+str(sensornumber)
        
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    cursor.execute('SELECT processed, unixtime, hour from %s' %(sensor))
    x=0
    z1=cursor.fetchall()
    ##print len(z)
    for count in z1:
        if float(count[0])==1:
            x+=1
        if int(count[2])>=5 and int(count[2])<=20:
            if float(count[0])<=1:
                data1.append('nan')
            else:
                data1.append(float(count[0]))
        elif int(count[2])<5 or int(count[2])>20:
            data1.append(float(count[0]))
        time1.append(float(count[1]))
        hour1.append(float(count[2]))
        
    #print len(data)
    for count in range(len(data1)):
        if time1[count]-time1[count-1]<=6*300000 and data1[count]=='nan':
            if data1[count-1]!='nan':
                data1[count]=data1[count-1]
            else:
                data1[count]=1
            #data1[count]=np.mean(data1[count-2:count-1])
        elif time1[count]-time1[count-1]>6*300000 and data1[count]=='nan':
            data1[count]=1
            
    #rate of change
    for t in range(len(data1)-1):
        rate=data1[t+1]-data1[t]
        ROC1.append(rate)
        
    #rate of rate of change
    for n in range(len(ROC1)-1):
        changeofrate=ROC1[n+1]-ROC1[n]
        RROC1.append(changeofrate)
        
    #moving mean and standard deviation
    w= movingStatsWindow
    count=0
    while count<=w-1:
        average=np.mean(data1[count:w])
        std=np.std(data1[count:w])
        mean1.append((average, time1[count]))
        stdev1.append(std)
        count+=1
    count=w
    while count<=(len(data1)-w):
        average=np.mean(data1[count-w:count+w])
        std=np.std(data1[count-w:count+w])
        mean1.append((average, time1[count]))
        stdev1.append(std)
        count+=1
    while count>=len(data1)-w+1 and count<len(data1):
        average=np.mean(data1[count:len(data1)])
        std=np.std(data1[count:len(data1)])
        mean1.append((average,time1[count]))
        stdev1.append(std)
        count+=1
    for count in range(len(data1)):
        if data1[count]=='nan' or mean1[count]=='nan':
            print("WHAT THE HECK")

    p=expWindow
    alpha=Alpha

    for count in range(len(data1)):
        addsum1=0
        for add in range(p-1):
            term=float(alpha)*math.pow((1-float(alpha)),add)*data1[count-add]
            addsum1+=term
        smoothed=addsum1+math.pow((1-float(alpha)),p)*data1[count-p]
        esmooth1.append((smoothed,time1[count]))


    final=[time1,data1,mean1,esmooth1,stdev1]
    if smoothtype=='exponential':
        output=final[3]
    elif smoothtype=='average':
        output=final[2]

    return output


def smoothingtables():
    """This command smoothes all the BEST lab light data and the
    NASA light data by calling the smoothing function. It performs
    both types of smoothing including exponential and average. """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    hesse_tables = [1,2,3,4]
    types = ['exponential', 'average']
    for elem in tables:
        table = 'light' + str(elem)
        print table
        for element in types:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            x = smoothing(elem, 'Hesse', element)
            for part in x:
                cursor.execute('UPDATE ' + str(table) + ' SET ' + str(element) + ' = ' + str(part[0]) + ' WHERE unixtime = ' + str(part[1]))
            connection.commit()
    newcitris_tables = [5, 6, 7, 8, 9, 10]
    for elem in tables:
        table = 'light' + str(elem)
        print table
        for element in types:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            x = smoothing(elem, 'NewCitris', element)
            for part in x:
                cursor.execute('UPDATE ' + str(table) + ' SET ' + str(element) + ' = ' + str(part[0]) + ' WHERE unixtime = ' + str(part[1]))
            connection.commit()
    nasa_tables = [1,2,3,4,5,6,7,8,9]
    for elem in nasa_tables:
        table = 'nasalight' + str(elem)
        print table
        for element in types:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            x = smoothing(elem, 'NASA', element)
            for part in x:
                cursor.execute('UPDATE ' + str(table) + ' SET ' + str(element) + ' = ' + str(part[0]) + ' WHERE unixtime = ' + str(part[1]))
            connection.commit()
    new_nasa_tables = [1,2,3,4,5,6,7]
    for elem in nasa_tables:
        table = 'newnasalight' + str(elem)
        print table
        for element in types:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            x = smoothing(elem, 'NewNasa', element)
            for part in x:
                cursor.execute('UPDATE ' + str(table) + ' SET ' + str(element) + ' = ' + str(part[0]) + ' WHERE unixtime = ' + str(part[1]))
            connection.commit()


#############################
### CLUSTERING LIGHT DATA ###
#############################


def inter(start,end):
    interval = [start]
    while interval[-1] < end:
        interval.append(interval[-1]+1800000)
    return interval

def getdeviations(x, mean, stddev):
   return math.fabs(x - mean) / stddev

def classify(month, table):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    # 24 - 30 min intervals from hours 6 to 18
    intervals_avg = [[] for i in range(24)]
    intervals_std = [[] for i in range(24)]
    uncounted = []
    i = 0
    alldata = [[] for i in range(24)]
    for count in range(len(alldata)):
        alldata[count] = [[] for i in range(3)]
    while i < len(month) - 1:
        unix = month[i]
        unix_next = month[i+1]
        cursor.execute('SELECT AVG(light),hour,AVG(minute) FROM ' + str(table) + ' WHERE unixtime >= ' + str(unix) + ' AND unixtime < ' + str(unix_next) + ' AND hour >= 6 AND hour < 18')
        data = cursor.fetchall()
        if data[0] != (None,None,None):
            avg = data[0][0]
            cursor.execute('SELECT SUM((light- ' + str(avg) + ')*(light - ' + str(avg) + '))/COUNT(light) FROM ' + str(table) + ' WHERE unixtime >= ' + str(unix) + ' AND unixtime < ' + str(unix_next) + ' AND hour >= 6 AND hour < 18')
            variance = cursor.fetchall()
            std = np.sqrt(variance)
            if data[0][2] < 30:
                intervals_avg[2*(data[0][1]-6)].append(avg)
                intervals_std[2*(data[0][1]-6)].append(std)
            elif data[0][2] >= 30 and data[0][2] < 60:
                intervals_avg[2*(data[0][1]-6)+1].append(avg)
                intervals_std[2*(data[0][1]-6)+1].append(std)
            else:
                uncounted.append(data[0])
        i+=1
    return intervals_avg,intervals_std


def cluster(table,start, end, cen_num = 3,iter_num = 100,n = 20):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    # cluster training period (dec 1 to apr 1)
    avgs,stds = classify(inter(start,end), table)
    a = 0
    while a < len(avgs):
        med = np.mean(avgs[a])
        std = np.std(avgs[a])
        i = 0
        while i < len(avgs[a]):
            if getdeviations(avgs[a][i], med, std) > 1 or stds[a][i] > avgs[a][i]:
                avgs[a].pop(i)
                stds[a].pop(i)
                i-=1
            i+=1
        a+=1
    
    #colors
    cs = [[1,0,0],[0,1,0],[0,0,1],[0,1,1],[1,1,0],[1,0,1],[0,0,0]]
    allcentroids = []
    #run kmeans (choose int_num and cen_num and iter_num)
    for int_num in range(1):
        #cen_num = 3
        #iter_num = 300
        #run kmeans n-times (different initialization points each time)
        #n = 60
        centroids = []
        ##stdss = stds[int_num]
        stdss = [stds[int_num][count]/avgs[int_num][count] for count in range(len(stds[int_num]))]
        allpoints = np.array(zip(avgs[int_num],stdss))#stds[int_num]))
        if n > 1:
            Js = []
            labs = []
            plt.figure()
            plt.scatter(avgs[int_num],stdss,c=cs[6])
            for i in range(n):
                dists = []
                centroid,lab = kmeans2(allpoints,cen_num,iter_num,minit='points')
                labs.append(lab)
                centroids.append(centroid)
                x = list(centroids[i][:,0])
                y = list(centroids[i][:,1])
                a = list(centroids[i][:,0])
                b = list(centroids[i][:,1])
                for rep in range(len(a)):
                    for cen in range(len(a)-1):
                        if a[cen] > a[cen+1]:
                            x[cen] = a[cen+1]
                            y[cen] = b[cen+1]
                            x[cen+1] = a[cen]
                            y[cen+1] = b[cen]              
                        a = list(x)
                        b = list(y)
                #plt.scatter(x,y,s=30*(n-i),c=cs[:cen_num])
                for count in range(len(allpoints)):
                    dist = np.linalg.norm(allpoints[count]-centroid[lab[count]])
                    dists.append(dist)
                J = 1.0/float(len(allpoints))*np.sum(np.array(dists)**2)
                Js.append(J)
            # centroid stores all n centroids
            centroid = centroids
            # just the one with min J
            plt.scatter(centroid[np.argmin(Js)][:,0],centroid[np.argmin(Js)][:,1],s=200,c=cs[:cen_num])
            colors = ([(cs[:cen_num])[j] for j in labs[np.argmin(Js)]])
            plt.scatter(avgs[int_num],stdss,c=colors)
            centroid = centroid[np.argmin(Js)]
        else:
            centroid,lab = kmeans2(allpoints,cen_num,iter_num,minit='points')
            colors = ([(cs[:cen_num])[j] for j in lab])
            plt.scatter(avgs[int_num],stds[int_num],c=colors)
            plt.scatter(centroid[:,0],centroid[:,1],s=100,c=cs[:cen_num])
            #plt.savefig('D:/Ben/Downloads/Classify/cluster.png')
            dists = []
            for count in range(len(allpoints)):
                dist = np.linalg.norm(allpoints[count]-centroid[lab[count]])
                dists.append(dist)
            J = 1.0/float(len(allpoints))*np.sum(np.array(dists)**2)
        allcentroids.append(centroid)
    plt.xlabel("Mean Illuminance (lux)")
    plt.ylabel("Standard Deviation of Illuminance (lux)")
    #path = "./nasalight1-interval" + str(i)
    #save(path, ext="png", close=True, verbose=False)
    plt.show()
    return allcentroids


def whereisit(light,interval,acs,n=3):
    avg = np.mean(light)
    std = np.std(light)
    point = np.array([avg,std])
    dists = []
    for count in range(n):
        dist = np.linalg.norm(point - acs[interval][count])
        dists.append(dist)
    tag = interval*n+np.argmin(dists)
    return tag


def intervals(table, start, end):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT light, hour, minute, day, unixtime FROM ' + str(table) + ' WHERE unixtime > ' + str(start) + ' AND unixtime < ' + str(end) + ' AND hour >= 6 AND hour < 18')
    data = cursor.fetchall()
    intervals = [[] for i in range(24)]
    for i in range(24):
        intervals[i].append([])
    current = data[0][3]
    counter = [0 for i in range(24)]
    for count in range(len(data)):
        if data[count][2] < 30:
            if current != data[count][3]:
                counter[2*(data[count][1]-6)]+=1
                intervals[2*(data[count][1]-6)].append([])
            intervals[2*(data[count][1]-6)][counter[2*(data[count][1]-6)]].append(data[count])
        elif data[count][2] >= 30 and data[count][2] < 60:
            if current != data[count][3]:
                counter[2*(data[count][1]-6)+1]+=1
                intervals[2*(data[count][1]-6)+1].append([])
            intervals[2*(data[count][1]-6)+1][counter[2*(data[count][1]-6)+1]].append(data[count])
        current = data[count][3]
    return intervals

def create_cluster(table, start, end, cluster_results):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    results = intervals(table, start, end)
    #0-23 light intervals
    interval = 0
    for elem in results:
        #Each 30 minute interval
        for element in elem:
            lights = []
            unixtimes = []
            if len(element) != 0:
                first = element[0][4]
                last = element[-1][4]
                #if last - first <= 1800000:
                    #Every tuple
                for i in element:
                    lights.append(i[0])
                    unixtimes.append(i[4])
                cluster = whereisit(lights, interval,cluster_results)
                for time in unixtimes:
                    cursor.execute('UPDATE ' + str(table) + ' SET cluster = ' + str(cluster) + ' WHERE unixtime = ' + str(time))
                connection.commit()
        interval+=1            


def update_clusters(table):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    if table == 'light1':
        tables = ['light2', 'light3', 'light4']
    elif table == 'light8':
        tables = ['light5', 'light6', 'light7', 'light9', 'light10']
    elif table == ['newnasalight1']:
        tables = ['newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7']
    else:
        tables = ['nasalight1', 'nasalight2', 'nasalight3', 'nasalight4', 'nasalight5', 'nasalight6', 'nasalight7', 'nasalight9']
    for other_tables in tables:
        a = cursor.execute('SELECT cluster, unixtime FROM ' + str(table) + ' WHERE cluster >= 0')
        y = a.fetchall()
        for elem in y:
            c = cursor.execute('SELECT unixtime FROM ' +str(other_tables)+ ' WHERE unixtime >= -150000 + ' + str(elem[1]) + ' AND unixtime <= 150000 + ' + str(elem[1]))
            x = c.fetchall()
            if len(x) > 0:
                cursor.execute('UPDATE ' + str(other_tables) + ' SET cluster = ' + str(elem[0]) + ' WHERE unixtime >= -150000 + ' + str(elem[1]) + ' AND unixtime < 150000 + ' + str(elem[1]))  
        connection.commit()    

#############################
### SOFT CLUSTERING #########
#############################

from random import sample

def new_classify(month, table):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    # 24 - 30 min intervals from hours 6 to 18
    intervals_avg = [[] for i in range(24)]
    intervals_std = [[] for i in range(24)]
    intervals_time = [[] for i in range(24)] 
    uncounted = []
    i = 0
    alldata = [[] for i in range(24)]
    for count in range(len(alldata)):
        alldata[count] = [[] for i in range(3)]
    while i < len(month) - 1:
        unix = month[i]
        unix_next = month[i+1]
        cursor.execute('SELECT AVG(light),hour,AVG(minute) FROM ' + str(table) + ' WHERE unixtime >= ' + str(unix) + ' AND unixtime < ' + str(unix_next) + ' AND hour >= 6 AND hour < 18')
        data = cursor.fetchall()
        if data[0] != (None,None,None):
            avg = data[0][0]
            cursor.execute('SELECT SUM((light- ' + str(avg) + ')*(light - ' + str(avg) + '))/COUNT(light) FROM ' + str(table) + ' WHERE unixtime >= ' + str(unix) + ' AND unixtime < ' + str(unix_next) + ' AND hour >= 6 AND hour < 18')
            variance = cursor.fetchall()
            std = np.sqrt(variance)[0][0]
            if data[0][2] < 30:
                intervals_avg[2*(data[0][1]-6)].append(avg)
                intervals_std[2*(data[0][1]-6)].append(std)
                intervals_time[2*(data[0][1]-6)].append((unix, unix_next))
            elif data[0][2] >= 30 and data[0][2] < 60:
                intervals_avg[2*(data[0][1]-6)+1].append(avg)
                intervals_std[2*(data[0][1]-6)+1].append(std)
                intervals_time[2*(data[0][1]-6)+1].append((unix, unix_next))
            else:
                uncounted.append(data[0])
        i+=1
    avgs,stds, time = intervals_avg,intervals_std, intervals_time
    a = 0
    while a < len(avgs):
        med = np.mean(avgs[a])
        std = np.std(avgs[a])
        i = 0
        while i < len(avgs[a]):
            if getdeviations(avgs[a][i], med, std) > 1 or stds[a][i] > avgs[a][i]:
                avgs[a].pop(i)
                stds[a].pop(i)
                time[a].pop(i)                            
                i-=1
            i+=1
        a+=1
    return avgs, stds, time


def fuzzy(data_mean, data_std):
    data = (np.vstack([data_mean, data_std])).T
    #Initialize centroid
    init_cen= sample(data,3)
    #Initialize membership matrix
    m=2 #fuzzy coefficient
    init_mem_new=np.random.rand(len(data),len(init_cen))
    num=0
    diff=np.empty((len(data),len(init_cen)))
    #diff=[[]]
    tol=0.05
    diffmax=2
    #print init_mem_new
    while diffmax>tol:
        diffarray=[]
        init_mem=[row[:] for row in init_mem_new]
        init_mem=np.vstack(init_mem[0:])
        #print "membership fn: ", init_mem
        #compute centroid
        for j in range(len(init_cen)):
            k =len(init_cen[j])
            num = np.zeros(2)
            #print num
            den=0
            for i in range(len(data)):
                compo1=math.pow(init_mem[i][j],2)*data[i]
                for k in range(len(compo1)):
                    num[k]+=compo1[k]
                compo2=math.pow(init_mem[i][j],2)
                den+=compo2
            init_cen[j]=num/den
            #print num,den,init_cen[j]
            #print init_cen
        for i in range(len(data)):
            den=0
            for j in range(len(init_cen)):
                #print data[i],init_cen[j]
                for k in range(len(data[i])):
                    if data[i][k]!=init_cen[j][k]:
                        compo=math.pow(1/np.linalg.norm(data[i]-init_cen[j]),2/(m-1))
                        
                    else:
                        compo=math.pow(1/np.linalg.norm(data[i]+1-init_cen[j]),2/(m-1))
                        #print 'bad'
                #print init_cen[j],compo
                den+=compo
            for j in range(len(init_cen)):
                num=math.pow(np.linalg.norm(data[i]-init_cen[j]),2/(m-1))
                for k in range(len(data[i])):
                    if data[i][k]!=init_cen[j][k]:
                        init_mem_new[i][j]=1/(num*den)
                    else:
                        init_mem_new[i][j]==1
            #print sum(init_mem_new[i])
        diff=[abs(i-j) for i,j in zip(init_mem_new,init_mem)]
        #print diff
        diff=np.vstack((diff[0:]))
        #print diff
        for i in range(len(data)):
            diffarray.append(max(diff[i]))
        #print diffarray
        diffmax=max(diffarray)
        #print 'showing steps', diffmax    
    return init_mem, init_cen        

def find_element_in_list(element,list_element):
    try:
        index_element=list_element.index(element)
        return index_element
    except ValueError:
        return -1       

def soft_cluster(testbed):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    if testbed == 'NASA':
        tables = ['nasalight1', 'nasalight2', 'nasalight3', 'nasalight4', 'nasalight5', 'nasalight6', 'nasalight7', 'nasalight8', 'nasalight9']
        month = inter(1337842800000,1358409600000)
    elif testbed == 'Hesse':
        tables = ['light1', 'light2', 'light3', 'light4']
        month = inter(1354370571000.0,1364777853000.0)
    elif testbed == 'NewCitris':
        tables = ['light1', 'light2', 'light3', 'light4', 'light5', 'light6', 'light7', 'light8', 'light9', 'light10']
        month = inter(1354370571000.0,1364777853000.0)
    else:
        tables = ['newnasalight1', 'newnasalight2', 'newnasalight3', 'newnasalight4', 'newnasalight5', 'newnasalight6', 'newnasalight7']
        month = inter(1354370571000.0,1364777853000.0)
    for table in tables:
        print table
        avgs, stds, time = new_classify(month, table)
        for interval in range(24):
            soft1, soft2, soft3 = (interval * 3), ((interval * 3) + 1), ((interval*3) + 2)
            data_mean, data_std = avgs[interval], stds[interval]
            membership, centroids = fuzzy(data_mean, data_std)
            original = [centroids[0][0], centroids[1][0], centroids[2][0]]
            order = sorted(original)
            new_order = []
            for elem in order:
                x = find_element_in_list(elem, original)
                new_order.append(x)
            index_1, index_2, index_3 = new_order[0], new_order[1], new_order[2]
            i = 0
            while i < len(membership):
                start = time[interval][i][0]
                end = time[interval][i][1]
                mem1 = membership[i][index_1]
                mem2 = membership[i][index_2]
                mem3 = membership[i][index_3]
                cursor.execute('UPDATE ' + str(table) + ' SET soft1 = ' + str(soft1) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                cursor.execute('UPDATE ' + str(table) + ' SET soft2 = ' + str(soft2) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                cursor.execute('UPDATE ' + str(table) + ' SET soft3 = ' + str(soft3) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                cursor.execute('UPDATE ' + str(table) + ' SET mem1 = ' + str(mem1) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                cursor.execute('UPDATE ' + str(table) + ' SET mem2 = ' + str(mem2) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                cursor.execute('UPDATE ' + str(table) + ' SET mem3 = ' + str(mem3) + ' WHERE unixtime >= ' + str(start) + ' AND unixtime <= ' + str(end))
                i+=1
            connection.commit()
        
        
##############################
### ARTIFICIAL LIGHT DATA  ###
##############################

LightA = [(1337950800000,100), (1337997900000, 100), (1337998260000,0),(1338210000000,100),

        (1338257100000,100),(1338257460000,0),(1338296400000,100),(1338343500000,100),

        (1338343860000,0),(1338382800000,100),(1338426900000,0),(1338429900000,0),

        (1338469200000,100),(1338516300000,100),(1338516600000,0),(1338555600000,100),

        (1338602700000,100),(1338603060000,0),(1338814800000,100),(1338861900000,100),

        (1338862260000,0),(1338901200000,100),(1338948300000,100),(1338948660000,0),

        (1338987600000,100),(1339034700000,100),(1339035000000,0),(1339074000000,100),

        (1339121100000,100),(1339121460000, 0),(1339160400000, 100),(1339171440000,0)]

LightB = [(1337950800000,100),(1337997900000,100),(1337998260000,0), (1338210000000,100),
          (1338257100000,100),(1338257460000,0),(1338296400000,100),(1338343500000,100),
          (1338343860000,0),(1338382800000,100),(1338426900000,88),(1338426960000,0),
          (1338429900000,0),(1338469200000,100),(1338516300000,100),(1338516600000,0),
          (1338555600000,100),(1338602700000,100),(1338603060000,0),(1338814800000,100),
          (1338861900000,100),(1338862260000,0),(1338901200000,100),(1338948300000,100),
          (1338948660000,0),(1338987600000,100),(1339034700000,100),(1339035000000,0),
          (1339074000000,100),(1339121100000,100),(1339121460000, 0),(1339160400000, 100),
          (1339171440000,100),(1339205460000,0)]

LightC = [(1337950800000,100), (1337997900000, 100), (1337998260000,0),(1338210000000,100),
          (1338257100000,100),(1338257460000,0),(1338296400000,100),(1338343500000,100),
          (1338343860000,0),(1338382800000,100),(1338391320000, 0),(1338426900000,0),
          (1338429900000,0),(1338430260000,0),(1338469200000,100),(1338516300000,100),
          (1338516600000,0),(1338555600000,100),(1338602700000,100),(1338603060000,0),(1338814800000,100),
          (1338861900000,100),(1338862260000,0),(1338901200000,100),(1338948300000,100),(1338948660000,0),
          (1338987600000,100),(1339034700000,100),(1339035000000,0),(1339074000000,100),(1339081980000,0),
          (1339121100000,0),(1339160400000, 100),(1339205460000,0)]


LightD = [(1337950800000,100), (1337997900000, 100), (1337998260000,0),(1338210000000,100),
          (1338257100000,100),(1338257460000,0),(1338296400000,100),(1338343500000,100),
          (1338343860000,0),(1338382800000,100),(1338391320000,0),(1338426900000,0),
          (1338429900000,0),(1338430260000,0),(1338469200000,100),(1338516300000,100),
          (1338516600000,0),(1338555600000,100),(1338602700000,100),(1338603060000,0),
          (1338814800000,100),(1338861900000,100),(1338862600000,0),(1338901200000,100),
          (1338933960000,0),(1338948300000,0),(1338987600000,100),(1339003200000,0),
          (1339034700000,0),(1339074000000,100),(1339081980000,0),(1339121100000,0),
          (1339160400000,100),(1339171020000,0)]

##Additional Light Data##
NewLightA = [(1339419600000.0, 100.0), (1339466700000.0, 100.0), (1339467060000.0, 0.0), (1339472220000.0, 100.0), (1339472220000.0, 88.0),
             (1339472280000.0, 100.0), (1339472280000.0, 0.0), (1339479780000.0, 0.0), (1339506000000.0, 100.0), (1339553100000.0, 100.0),
             (1339553460000.0, 0.0), (1339592400000.0, 100.0), (1339639500000.0, 100.0), (1339639800000.0, 0.0), (1339678800000.0, 100.0),
             (1339725900000.0, 100.0), (1339726260000.0, 0.0), (1339734240000.0, 100.0), (1339734240000.0, 0.0), (1339745760000.0, 0.0), (1339765200000.0, 100.0),
             (1339790940000.0, 0.0), (1339812300000.0, 0.0), (1339822440000.0, 100.0), (1339822800000.0, 0.0), (1339830360000.0, 0.0), (1340024400000.0, 100.0),
             (1340071500000.0, 100.0), (1340071860000.0, 0.0), (1340079540000.0, 100.0), (1340080200000.0, 0.0), (1340087700000.0, 0.0), (1340110800000.0, 100.0),
             (1340157900000.0, 100.0), (1340158260000.0, 0.0), (1340197200000.0, 100.0), (1340244300000.0, 100.0), (1340244600000.0, 0.0), (1340283600000.0, 100.0),
             (1340330700000.0, 100.0), (1340331060000.0, 0.0), (1340370000000.0, 100.0), (1340417100000.0, 100.0), (1340417460000.0, 0.0), (1340422260000.0, 100.0),
             (1340429760000.0, 100.0), (1340437020000.0, 100.0), (1340437320000.0, 0.0), (1340629200000.0, 100.0), (1340676300000.0, 100.0), (1340676660000.0, 0.0),
             (1340715600000.0, 100.0), (1340762700000.0, 100.0), (1340763060000.0, 0.0), (1340768100000.0, 100.0), (1340768160000.0, 0.0), (1340778900000.0, 0.0),
             (1340802000000.0, 100.0), (1340849100000.0, 100.0), (1340849460000.0, 0.0), (1340888400000.0, 100.0), (1340935500000.0, 100.0), (1340935860000.0, 0.0),
             (1340974800000.0, 100.0), (1341021900000.0, 100.0), (1341022260000.0, 0.0)]

NewLightB = [(1339419600000.0, 100.0), (1339466700000.0, 100.0), (1339467060000.0, 0.0), (1339472220000.0, 100.0), (1339472220000.0, 88.0), (1339472280000.0, 100.0),
             (1339472280000.0, 0.0), (1339479780000.0, 0.0), (1339506000000.0, 100.0), (1339553100000.0, 100.0), (1339553460000.0, 0.0), (1339592400000.0, 100.0),
             (1339639500000.0, 100.0), (1339639800000.0, 0.0), (1339678800000.0, 100.0), (1339725900000.0, 100.0), (1339726260000.0, 0.0), (1339734240000.0, 100.0),
             (1339734240000.0, 0.0), (1339745760000.0, 0.0), (1339765200000.0, 100.0), (1339790940000.0, 0.0), (1339790940000.0, 100.0), (1339812300000.0, 100.0),
             (1339812660000.0, 0.0), (1339822440000.0, 100.0), (1339822800000.0, 0.0), (1339830360000.0, 0.0), (1340024400000.0, 100.0), (1340071500000.0, 100.0),
             (1340071860000.0, 0.0), (1340079540000.0, 100.0), (1340080200000.0, 0.0), (1340087700000.0, 0.0), (1340110800000.0, 100.0), (1340157900000.0, 100.0),
             (1340158260000.0, 0.0), (1340197200000.0, 100.0), (1340244300000.0, 100.0), (1340244600000.0, 0.0), (1340283600000.0, 100.0), (1340330700000.0, 100.0),
             (1340331060000.0, 0.0), (1340370000000.0, 100.0), (1340417100000.0, 100.0), (1340417460000.0, 0.0), (1340422260000.0, 100.0), (1340429760000.0, 100.0),
             (1340437020000.0, 100.0), (1340437320000.0, 0.0), (1340629200000.0, 100.0), (1340676300000.0, 100.0), (1340676660000.0, 0.0), (1340715600000.0, 100.0),
             (1340762700000.0, 100.0), (1340763060000.0, 0.0), (1340768100000.0, 100.0), (1340768160000.0, 0.0), (1340778900000.0, 0.0), (1340802000000.0, 100.0),
             (1340849100000.0, 100.0), (1340849460000.0, 0.0), (1340888400000.0, 100.0), (1340935500000.0, 100.0), (1340935860000.0, 0.0), (1340974800000.0, 100.0),
             (1341021900000.0, 100.0), (1341022260000.0, 0.0)]

NewLightC= [(1339419600000.0, 100.0), (1339428540000.0, 0.0), (1339466700000.0, 0.0), (1339472220000.0, 100.0), (1339472220000.0, 0.0), (1339472220000.0, 100.0),
            (1339472220000.0, 0.0), (1339472220000.0, 2.0), (1339472280000.0, 0.0), (1339479780000.0, 0.0), (1339506000000.0, 100.0), (1339550280000.0, 0.0),
            (1339553100000.0, 0.0), (1339592400000.0, 100.0), (1339627560000.0, 0.0), (1339627560000.0, 100.0), (1339639500000.0, 100.0), (1339639800000.0, 0.0),
            (1339678800000.0, 100.0), (1339725900000.0, 100.0), (1339726260000.0, 0.0), (1339734240000.0, 100.0), (1339734240000.0, 0.0), (1339734240000.0, 100.0),
            (1339738260000.0, 0.0), (1339745760000.0, 0.0), (1339765200000.0, 100.0), (1339790940000.0, 0.0), (1339812300000.0, 0.0), (1339822440000.0, 100.0),
            (1339822860000.0, 0.0), (1339830360000.0, 0.0), (1340024400000.0, 100.0), (1340057280000.0, 0.0), (1340057280000.0, 100.0), (1340071500000.0, 100.0),
            (1340071860000.0, 0.0), (1340079540000.0, 100.0), (1340080140000.0, 0.0), (1340087700000.0, 0.0), (1340110800000.0, 100.0), (1340121660000.0, 0.0),
            (1340157900000.0, 0.0), (1340197200000.0, 100.0), (1340204100000.0, 0.0), (1340244300000.0, 0.0), (1340283600000.0, 100.0), (1340330700000.0, 100.0),
            (1340331060000.0, 0.0), (1340370000000.0, 100.0), (1340412240000.0, 0.0), (1340417100000.0, 0.0), (1340422260000.0, 100.0), (1340429760000.0, 100.0),
            (1340437020000.0, 100.0), (1340437320000.0, 0.0), (1340629200000.0, 100.0), (1340676300000.0, 100.0), (1340676660000.0, 0.0), (1340715600000.0, 100.0),
            (1340762700000.0, 100.0), (1340763060000.0, 0.0), (1340768100000.0, 100.0), (1340768100000.0, 0.0), (1340768160000.0, 100.0), (1340768160000.0, 0.0),
            (1340778900000.0, 0.0), (1340802000000.0, 100.0), (1340849100000.0, 100.0), (1340849460000.0, 0.0), (1340888400000.0, 100.0), (1340935500000.0, 100.0),
            (1340935860000.0, 0.0), (1340974800000.0, 100.0), (1341021900000.0, 100.0), (1341022260000.0, 0.0)]

NewLightD = [(1339419600000.0, 100.0), (1339428540000.0, 0.0), (1339466700000.0, 0.0), (1339472220000.0, 100.0), (1339472220000.0, 0.0), (1339472220000.0, 100.0),
             (1339472220000.0, 0.0), (1339472220000.0, 2.0), (1339472220000.0, 100.0), (1339472220000.0, 0.0), (1339479780000.0, 0.0), (1339506000000.0, 100.0),
             (1339529460000.0, 0.0), (1339553100000.0, 0.0), (1339592400000.0, 100.0), (1339627560000.0, 0.0), (1339639500000.0, 0.0), (1339678800000.0, 100.0),
             (1339705200000.0, 0.0), (1339725900000.0, 0.0), (1339734240000.0, 0.0), (1339745760000.0, 0.0), (1339765200000.0, 100.0), (1339783740000.0, 0.0),
             (1339812300000.0, 0.0), (1339822440000.0, 100.0), (1339822800000.0, 0.0), (1339830360000.0, 0.0), (1340024400000.0, 100.0), (1340057280000.0, 0.0),
             (1340071500000.0, 0.0), (1340079540000.0, 100.0), (1340080140000.0, 0.0), (1340087700000.0, 0.0), (1340110800000.0, 100.0), (1340121660000.0, 0.0),
             (1340157900000.0, 0.0), (1340197200000.0, 100.0), (1340204100000.0, 0.0), (1340244300000.0, 0.0), (1340283600000.0, 100.0), (1340330700000.0, 100.0),
             (1340331060000.0, 0.0), (1340370000000.0, 100.0), (1340412240000.0, 0.0), (1340417100000.0, 0.0), (1340422260000.0, 100.0), (1340429520000.0, 0.0),
             (1340437020000.0, 0.0), (1340629200000.0, 100.0), (1340676300000.0, 100.0), (1340676660000.0, 0.0), (1340715600000.0, 100.0), (1340762700000.0, 100.0),
             (1340763060000.0, 0.0), (1340768100000.0, 100.0), (1340768100000.0, 0.0), (1340768160000.0, 100.0), (1340771340000.0, 0.0), (1340778900000.0, 0.0),
             (1340802000000.0, 100.0), (1340849100000.0, 100.0), (1340849460000.0, 0.0), (1340888400000.0, 100.0), (1340935500000.0, 100.0), (1340935860000.0, 0.0),
             (1340974800000.0, 100.0), (1340982900000.0, 0.0), (1341021900000.0, 0.0)]


def create_artificial(old):
    letters = ['a','b','c','d']
    for elem in letters:
        table = 'light' + str(elem)
        print table
        if table == 'lighta':
            if old:
                data = LightA
            else:
                data = NewLightA
        if table == 'lightb':
            if old:
                data = LightB
            else:
                data = NewLightB
        if table == 'lightc':
            if old:
                data = LightC
            else:
                data = NewLightC
        if table == 'lightd':
            if old:
                data = LightD
            else:
                data = NewLightD
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        i = 0
        while i < (len(data) - 1):
            unix = data[i][0]
            artificial = data[i][1]
            next_unix = data[i+1][0]
            while unix < next_unix:
                ttb = time.localtime(float(unix/1000))
                tim=strftime("%a %d %m %Y %H %M %S",ttb)
                t = tim.split()
                sunpos = getSunpos(nasa_lat, nasa_lon, nasa_timezone, t[3], t[2],
                                   t[1], t[4], t[5], t[6])
                to_db = [unix, t[0], t[1], t[2], t[3],
                             t[4], t[5],t[6], artificial, sunpos[0],
                             sunpos[1], 'Nan', 'Nan', artificial, float('Nan')]
                cursor.execute('INSERT OR IGNORE INTO ' + str(table) + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', to_db)
                unix = unix + 300000
            i+=1
        unix = data[i][0]
        artificial = data[i][1]
        next_unix = 1339225199000
        while unix < next_unix:
                ttb = time.localtime(float(unix/1000))
                tim=strftime("%a %d %m %Y %H %M %S",ttb)
                t = tim.split()
                sunpos = getSunpos(nasa_lat, nasa_lon, nasa_timezone, t[3], t[2],
                                   t[1], t[4], t[5], t[6])
                to_db = [unix, t[0], t[1], t[2], t[3],
                             t[4], t[5],t[6], artificial, sunpos[0],
                             sunpos[1], 'Nan', 'Nan', artificial, float('Nan')]
                cursor.execute('INSERT OR IGNORE INTO ' + str(table) + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', to_db)
                unix = unix + 300000
        connection.commit()

def artificial_clusters():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    other_tables = ['lighta', 'lightb', 'lightc', 'lightd']
    for other in other_tables:
        a = cursor.execute('SELECT cluster, unixtime FROM nasalight8 WHERE cluster >= 0')
        y = a.fetchall()
        for elem in y:
            cursor.execute('UPDATE ' + str(other) + ' SET cluster = ' + str(elem[0]) + ' WHERE unixtime >= -120000 + ' + str(elem[1]) + ' AND unixtime <= 120000 + ' + str(elem[1]))  
        connection.commit()    


####################
### SHORTCUT CODE ##
####################

def createDatabase():
    create_tables()
    createCloudData()
    createLightData()
    create_artificial(True)
    create_artificial(False)
    print "Clustering Artificial Light"
    artificial_clusters()
        
def updateDatabase():
    #updateCloudData()
    updateLightData()    

#taken from http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/
def save(path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.
 
    Parameters
    ----------
    path : string
        The path (and filename, without the extension) to save the
        figure to.
 
    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
 
    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.
 
    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.
 
    """
    
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'
 
    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
 
    # The final path to save to
    savepath = os.path.join(directory, filename)
 
    if verbose:
        print("Saving figure to '%s'..." % savepath),
 
    # Actually save the figure
    plt.savefig(savepath)
    
    # Close it
    if close:
        plt.close()
 
    if verbose:
        print("Done")

if __name__ == '__main__':
    #best_lat = "37 52 27.447"
    #best_lon = "122 15 33.3864 W"
    #best_timezone = "US/Pacific"
    createNewCitris(best_lat, best_lon, best_timezone)
    createNewNasa(nasa_lat, nasa_lon, nasa_timezone)
    createDatabase()

    #connection = sqlite3.connect('data.db')
    #cursor = connection.cursor()
    #cursor.execute('SELECT MIN(unixtime), MAX(unixtime) FROM nasalight1')
    #unixtimedata = cursor.fetchall()
    #minunixtime = unixtimedata[0][0]
    #maxunixtime = unixtimedata[0][1]
    #cluster('nasalight1', minunixtime, maxunixtime, cen_num = 3,iter_num = 100,n = 20)
