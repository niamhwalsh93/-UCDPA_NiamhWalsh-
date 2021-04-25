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

#Import csv file and create a pandas dataframe using the variable NBA
NBA = pd.read_csv("all_seasons.csv")

#Expand dataframe to show all columns
pd.set_option('display.expand_frame_repr', False)

#Print the head of the dataframe to get the first five lines
print(NBA.head())

#Print the shape of the dataframe to get number of rows and columns
print(NBA.shape)

#Display column names
print(NBA.columns)

#Print dataframe index
print(NBA.index)

#Checking for null values within the dataframe
print(NBA.isna())

#Count the number of NA values per column
print(NBA.isna().sum())

#Replace NA values with 0
NBA.fillna(0)

#Create a varialbe NBA_filtering and filter the dataframe to return all rows and specified number of columns by name
NBA_filtering = NBA.loc[ : , ["player_name", "team_abbreviation", "player_height", "player_weight", "pts", "season"]]

#Create a varialbe NBA_filtered and access all rows where the season is equal to 2019-20
NBA_filtered = NBA_filtering.loc[NBA_filtering["season"]== "2019-20"]

#Create a varialbe NBA_Players_index and set the index to be player name and sorting by ascending values
NBA_Players_index = NBA_filtered.set_index("player_name").sort_index(ascending=True)

#Print the head of the dataframe to get the first five lines
print(NBA_Players_index.head())

#Create a new column in the dataframe called BMI by multiplying player height column by player weight and divide by 1000
NBA_Players_index["BMI"] = (NBA_Players_index["player_height"] * NBA_Players_index["player_weight"])/1000

#Print the head of the dataframe to get the first five lines
print(NBA_Players_index.head())

#Use iterrows and looping to create a new column ”result” based on information in “BMI” column
for index, row in NBA_Players_index.iterrows():
    print(f'Index: {index}, BMI: {row.get("BMI", 0)}')
result = []
for value in NBA_Players_index["BMI"]:
    if value >= 25:
            result.append("Above Average")
    elif value < 25 and value > 24:
            result.append("Average")
    else:
            result.append("Below Average")
NBA_Players_index["Result"] = result

#Print dataframe
print(NBA_Players_index)

#Define a function & print the 50th percentile of the BMI column
def pct50(column):
    return column.quantile(0.5)
print(NBA_Players_index["BMI"].agg(pct50))
def pct50(column):
    return column.quantile(0.5)

#Define a function & print the 25th percentile of the BMI column
def pct25(column):
    return column.quantile(0.25)
print(NBA_Players_index["BMI"].agg(pct25))
def pct50(column):
    return column.quantile(0.25)

#Create a new variable Team_MMS and use groupby to to get the min max of players height and weight for each team
Team_MMS = NBA_Players_index.groupby("team_abbreviation")[["player_height","player_weight"]].agg([min, max])

#Print dataframe
print(Team_MMS)

#Create a new variable Mean and use groupby to to get the mean of players height and weight for each team
Mean = NBA_Players_index.groupby("team_abbreviation")[["player_height","player_weight"]].mean()

#Print dataframe
print(Mean)

#Create a variable LAM and access all rows where player name is Lamar Odom
LAM = NBA_filtering.loc[NBA_filtering["player_name"]== "Lamar Odom"]

#Create a variable LAM_index and set index to player name and sort by ascending values
LAM_index = LAM.set_index("season").sort_index(ascending=True)

#Print dataframe
print(LAM_index)


