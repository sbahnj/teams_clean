import re
import pandas as pd

import mysql.connector
import mysql as mysql
import requests
import unidecode as unidecode
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
engine = create_engine("mysql://"+"root"+":"+"Colormewild1!"+"@"+"localhost"+"/"+"team")



# Connection info for the database
mydb = mysql.connector.connect(

         host="localhost",
         user="root",

         ## Should do the password-hiding thing shown in the slides (??)
         password="Colormewild1!",

         database="team"

     )

mycursor = mydb.cursor()

# teams in tournaments from 2018 - 2021, urls both with and without trainer nationalities
sample_team_url = ["https://www.pikalytics.com/results/worlds18m"]


all_exported_teams = []
for url in sample_team_url:

     page = requests.get(url).text
     soup = BeautifulSoup(page, "html.parser")

     export_teams = soup.find_all("span", {"class" : "export-results-team"})
     all_exported_teams.append(export_teams)




teams_dict = {}
i = 0
for team in str(all_exported_teams).split("data-stringify='["):


     value_list_team = []

     team_id = i

     replace1 = str(team).replace("<span class=\"export-results-team\" data-stringify=", "")

     value_list_team.append(replace1.split("style")[0])



     teams_dict[team_id] = value_list_team

     i = i + 1



team_info_string = ""
for key in teams_dict:


     team_info_string = team_info_string + str(teams_dict[key])



pokemon_list = []
# need to get all names
for item in team_info_string.split("types"):

    pokemon_list.append(item)




pokemon_list_types = []
pokemon_list_names = []

for item in str(pokemon_list).split(":"):
    if "nature" in str(item):
        pokemon_list_names.append(item)



for item in str(pokemon_list).split("}"):


    if ", " in str(item):

        pokemon_list_types.append(item)


pokemon_full_list = []
value_list = []
r = 0

for name in pokemon_list_names:



    if r <= len(pokemon_list_types)-1:
        value_list = name + pokemon_list_types[r]
        pokemon_full_list.append(value_list)
        r = r + 1





all_pokemon = {i:pokemon_full_list[i] for i in range(0, len(pokemon_full_list))}



trainer_names_teams = []

# Get the trainer name for each team
for url in sample_team_url:

     page = requests.get(url).text
     soup = BeautifulSoup(page, "html.parser")

     trainer_links = soup.find_all("h2")


     for trainer in trainer_links:

         trainer_names_teams_string = unidecode.unidecode(trainer.text)

         trainer_names_teams_sub = unidecode.unidecode(re.sub(r'\([^)]*\)', '', trainer_names_teams_string))


         trainer_names_teams.append(trainer_names_teams_sub)


i = 0

p1 = 0
p2 = 1
p3 = 2
p4 = 3
p5 = 4
p6 = 5
team_table_dict = {}
for name in trainer_names_teams:



    team_table_dict[i] = " " + trainer_names_teams[i] + "," + str(p1) + ","  + str(p2) + "," + str(p3) + "," + str(p4) + "," + str(p5) + "," + str(p6)

    i = i + 1

    p1 = p1 + 6
    p2 = p2 + 6
    p3 = p3 + 6
    p4 = p4 + 6
    p5 = p5 + 6
    p6 = p6 + 6


# Load the Pokemon table into the db
sql = "INSERT INTO pokemon (pokemon_id, species_name, species_type) VALUES (%s, %s, %s)"

for key in all_pokemon:

          #need to generate a unique name_val for each pokemon

          name_val_p = key
          other_val1= all_pokemon.get(key).split(",")[0]
          other_val2 = all_pokemon.get(key).split("[")[1]


          all_vals_p = (name_val_p, other_val1, other_val2 )


          #mycursor.execute(sql, all_vals_p)

          #mydb.commit()


# Fills out the Team table
sql_teams = "INSERT INTO team (team_id, trainer_name, p1_id, p2_id, p3_id, p4_id, p5_id, p6_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

for key in team_table_dict:

          id_val = key
          team_trainer = team_table_dict.get(key).split(",")[0]
          team_p1 = team_table_dict.get(key).split(",")[1]
          team_p2 = team_table_dict.get(key).split(",")[2]
          team_p3 = team_table_dict.get(key).split(",")[3]
          team_p4 = team_table_dict.get(key).split(",")[4]
          team_p5 = team_table_dict.get(key).split(",")[5]
          team_p6 = team_table_dict.get(key).split(",")[6]



          all_vals_team = (id_val, team_trainer, team_p1, team_p2, team_p3, team_p4, team_p5, team_p6)

          #print(all_vals_team)


          #mycursor.execute(sql_teams, all_vals_team)

          #mydb.commit()

#make TeamID, pokemon_id table. Two columns long: teamID and pokemonIDs. Each teamID repeats six times.




# make the data into a dataframe
team_ids = []
pokemon_ids = []

# get a list of the team ids
for key in team_table_dict:
    team_ids.append(key)
    team_ids.append(key)
    team_ids.append(key)
    team_ids.append(key)
    team_ids.append(key)
    team_ids.append(key)



# get a list of the pokemon_ids
for key in team_table_dict:
    pokemon_id_string = (str(team_table_dict[key]).split(",")[1:7])
    pokemon_ids.append(pokemon_id_string)



data_list = []
# Creating the data frames
for pokemon_id in str(pokemon_ids).split(","):

    id_clean = str(pokemon_id).replace("[", "")
    id_clean2 = id_clean.replace("]", "")

    frame_row = [0, id_clean2]

    data_list.append(frame_row)


df = pd.DataFrame(data_list, columns=['team_id', 'pokemon_id'])


# Updating the team id
i = 0
for team_id in team_ids:

         df.at[i, "team_id"] = team_id
         i = i + 1


print(df)


# insert the dataframe into a table
df.to_sql("individual_pokemon", engine, if_exists="replace")
