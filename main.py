import re
import pandas as pd

import mysql.connector
import mysql as mysql
import requests
import unidecode as unidecode
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)

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

# teams in tournaments from 2016 - 2021, urls both with and without trainer nationalities
sample_team_url = ["https://www.pikalytics.com/results/pc25inv21"]


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
pokemon_list_abilities = []
pokemon_list_moves = []
pokemon_list_item = []
pokemon_can_gmax = []

for item in str(pokemon_list).split(":"):
    if "nature" in str(item):
        name_string = str(item.replace("\"nature\"", ""))

        no_quotation = name_string.replace("\"", "")
        no_comma = no_quotation.capitalize().replace(",", "")

        no_nums = no_comma.replace("%20", " ")

        pokemon_list_names.append(no_nums)



for item in str(pokemon_list).split("}"):


    if ", " in str(item):

        pokemon_list_types.append(item)


# find the ability, moves list, held item, can_gmax for each pokemon

# find the ability for each pokemon
for item in str(pokemon_list).split(","):

    if "ability" in str(item):
        ability_clean = item.replace("ability", "")
        ability_clean2 = ability_clean.replace(":", "")
        ability_clean3 = ability_clean2.replace("\"", "")
        pokemon_list_abilities.append(ability_clean3)

# find the moves list for each pokemon
for item in str(pokemon_list).split("]"):
    if "moves" in str(item):
        list = []
        list.append(item.split("moves")[1])
        pokemon_list_moves.append(list)

# find the held item for each pokemon
for item in str(pokemon_list).split(","):
    if "item" in item and "item_us" not in item:
        item_clean = str(item).replace("item\":", "")
        item_clean2 = item_clean.replace("\"", "")
        pokemon_list_item.append(item_clean2)


#get the can_gmax list for the pokemon



adjusted_names = []
for name in pokemon_list_names:

    boolean = False

    regex = "(.*)-gmax"

    match = re.match(regex, name)

    if match:
        boolean = True
        pokemon_can_gmax.append(boolean)


        adjusted_names.append(match.group(1))


    else:
        pokemon_can_gmax.append(boolean)

        adjusted_names.append(name)




#pokemon_full_list = []
# value_list = []
# r = 0
#
# for name in pokemon_list_names:
#
#
#
#     if r <= len(pokemon_list_types)-1:
#         value_list = name + pokemon_list_types[r] + "," + pokemon_list_abilities[r].replace("ability\":", "") + "," + str(pokemon_list_moves[r]) \
#                      + "," + pokemon_list_item[r] + "," + pokemon_can_gmax[r]
#         pokemon_full_list.append(value_list)
#         r = r + 1
#
#
#
#
#
# all_pokemon = {i:pokemon_full_list[i] for i in range(0, len(pokemon_full_list))}





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
# sql = "INSERT INTO pokemon (pokemon_id, species_name, species_type) VALUES (%s, %s, %s)"
#
# for key in all_pokemon:
#
#           #need to generate a unique name_val for each pokemon
#
#           name_val_p = key
#           other_val1= all_pokemon.get(key).split(",")[0]
#           other_val2 = all_pokemon.get(key).split("[")[1]
#
#
#           all_vals_p = (name_val_p, other_val1, other_val2 )


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





# insert the dataframe into a table
#df.to_sql("individual_pokemon", engine, if_exists="replace")


# make the pokemon dict into a dataframe
#all_pokemon_df = pd.DataFrame.from_dict(all_pokemon, orient="index")

#print(all_pokemon_df)

#insert the pokemon datafram into a table
#all_pokemon_df.to_sql("all_pokemon", engine, if_exists="replace")

#make a dataframe out of the pokemon info lists
data_list_all_pokemon = []
for pokemon_id in str(pokemon_ids).split(","):
    id_clean = str(pokemon_id).replace("[", "")
    id_clean2 = id_clean.replace("]", "")



    frame_row = [id_clean2, "2", "3", "4", "5"]



    data_list_all_pokemon.append(frame_row)

df_all_pokemon = pd.DataFrame(data_list_all_pokemon, columns=['pokemon_id', 'species_name', 'ability', "item", "can_gmax"])


# Updating the species name
i = 0
for name in adjusted_names:


    df_all_pokemon.at[i, "species_name"] = name
    i = i + 1

# updating the ability
i = 0
for ability in pokemon_list_abilities:


    df_all_pokemon.at[i, "ability"] = ability
    i = i + 1

#updating the item
i = 0
for item in pokemon_list_item:


    df_all_pokemon.at[i, "item"] = item
    i = i + 1

# updating the can_gmax
i = 0
for value in pokemon_can_gmax:


    df_all_pokemon.at[i, "can_gmax"] = value
    i = i + 1



#insert the pokemon datafram into a table
df_all_pokemon.to_sql("all_pokemon", engine, if_exists="replace")


#get info for has_move
moves_ids_list = []


pokemon_with_move = 0
for item in pokemon_list_moves:

    name_count = str(item).count("name")

    if name_count == 4:
        moves_ids_list.append(pokemon_with_move)
        moves_ids_list.append(pokemon_with_move)
        moves_ids_list.append(pokemon_with_move)
        moves_ids_list.append(pokemon_with_move)

        pokemon_with_move = pokemon_with_move + 1

    if name_count == 3:
        moves_ids_list.append(pokemon_with_move)
        moves_ids_list.append(pokemon_with_move)
        moves_ids_list.append(pokemon_with_move)

        pokemon_with_move = pokemon_with_move + 1


single_move = []
l = 0
for item in str(pokemon_list_moves).split("}"):
    single_move_clean = str(item).replace("]]", "")
    single_move_clean2 = single_move_clean.replace("\"", "")
    single_move_clean3 = single_move_clean2.replace("{name:", "")

    regex2 = "(.*),type:"

    match = re.match(regex2, single_move_clean3)

    if match:

        single_move_clean4 = match.group(1)
        single_move.append(single_move_clean4)



#make dataframe for HasMove
data_list_hasMove = []
for item in moves_ids_list:

    frame_row = [item, "0"]



    data_list_hasMove.append(frame_row)

df_hasMove = pd.DataFrame(data_list_hasMove, columns=['pokemon_id', 'move_name'])


# updating the moves
i = 0
for single in single_move:


    df_hasMove.at[i, "move_name"] = single
    i = i + 1


print(df_hasMove)

#insert the pokemon datafram into a table
df_hasMove.to_sql("has_move", engine, if_exists="replace")

