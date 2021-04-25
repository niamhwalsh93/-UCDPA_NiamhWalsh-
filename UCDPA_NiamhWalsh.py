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

#Create figure & axes
fig, ax = plt.subplots(figsize=(20, 6))

#Plotting a line chart and customising
ax.plot(LAM_index["pts"], marker="o",linestyle="-",color="b")

#Setting and cutomising plot lables and titles
ax.set_xlabel("Season")
ax.set_ylabel("Points Scored")
ax.set_title("Points Scored Across all Seasons played")

ax.annotate('Max Points Scored', xy=("2000-01", 17), xytext=("2000-01", 15),
            arrowprops=dict(facecolor='black', shrink=0.01))

#Save the plot
plt.savefig("Line Plot - Points Scored Across all Seasons played.jpg")

#Display the plot
plt.show()

#Groupby team abbreviation and count the number of seasons played per team
print(LAM.groupby("team_abbreviation")["season"].count())

#Create a nump array
y = np.array([1, 5, 7, 1])

#Create variables of lists to define lables/colors/explode
mylabels = ["DAL", "LAC", "LAL", "MIA"]
mycolors = ["c", "m", "g", "y"]
myexplode = [0, 0, 0.2, 0]

#Create a pie chart and customise using the variables defined above
plt.pie(y, labels = mylabels, colors = mycolors, explode = myexplode, autopct='%1.1f%%', shadow=True)

#Add a legend to the plot
plt.legend(title = "Team Abbreviations:",
           loc="center left",
           bbox_to_anchor=(1, 0, 0.5, 1))

#Add a title to the plot
plt.title("Lamar Odom - Percentage of time spent with each NBA team over the course of NBA career")

#Save the plot
plt.savefig("Pie Chart - Percentage of time spent with each NBA team over the course of NBA career.jpg")

#Display the plot
plt.show()

#Sort the dataframe by ascending values on the BMI column
NBA_Players_index_sorted = NBA_Players_index.sort_values(by="BMI", ascending=False)

#Print the dataframe
print(NBA_Players_index_sorted)

#Create a Bar Plot and customise accordingly
#Create figure & axes
ax = NBA_Players_index_sorted.head(10)["BMI"].plot(kind='bar', title ="Top 10 BMI per players",figsize=(15,10),legend=True, fontsize=12, rot=20)
ax.set_xlabel("Player Names",fontsize=12)
ax.set_ylabel("BMI",fontsize=12)

#Save the plot
plt.savefig("Bar Chart - Top 10 BMI per players.jpg")

#Display the plot
plt.show()

#Create figure & axes
fig, ax = plt.subplots(figsize=(20, 6))

#Create a histogram based on BMI columns and specify bin levels to 15,20,25,30

ax.hist(NBA_Players_index["BMI"], label="BMI",
        bins=[15, 20, 25, 30], color="yellow")


#Set x and y axis lables
ax.set_ylabel("# of Observations")
ax.set_xlabel("BMI")

#Set Title
ax.set_title("Number of Observation per Histogram Bin")

#Save the plot
plt.savefig("Histogram - Number of Observation per Histogram Bin.jpg")

#Display the plot
plt.show()

