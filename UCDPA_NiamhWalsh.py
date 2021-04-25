#Import the required libraries/packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine

#Create an engine called engine
engine = create_engine('sqlite:///database.sqlite')

#Assign a variable called table_names to equal the table names
table_names = engine.table_names()

#Print the Table Names
print(table_names)

#Open an engine connection
con = engine.connect()

#Run a SQL Query rs
rs = con.execute("SELECT * FROM Player")

#Assign a variable called df to equal the results of the above query
df = pd.DataFrame(rs.fetchall())

#Close the connection
con.close()

#Print the dataframe head to get the first five lines
print(df.head())

#Use context manager to open engine and run a Sql query saving the results to rs
with engine.connect() as con:
    rs = con.execute("SELECT player_name FROM Player")
    df = pd.DataFrame(rs.fetchmany(size=5))
    df.columns = rs.keys()

#Print the length of the dataframe
print(len(df))

#Print the head of the dataframe to get the first five lines
print(df.head())

