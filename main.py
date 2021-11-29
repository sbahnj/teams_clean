import re

import mysql.connector
import mysql as mysql
import requests
import unidecode as unidecode
from bs4 import BeautifulSoup

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
sample_team_url = ["https://www.pikalytics.com/results/worlds18m", "https://www.pikalytics.com/results/worlds18s",
                           "https://www.pikalytics.com/results/worlds18j", "https://www.pikalytics.com/results/naint18m",
                           "https://www.pikalytics.com/results/naint18s", "https://www.pikalytics.com/results/naint18j",
                           "https://www.pikalytics.com/results/latamint18m", "https://www.pikalytics.com/results/latamint18s",
                           "https://www.pikalytics.com/results/latamint18j", "https://www.pikalytics.com/results/oceareg18m",
                           "https://www.pikalytics.com/results/oceareg18s", "https://www.pikalytics.com/results/oceareg18j",
                           "https://www.pikalytics.com/results/naint19m", "https://www.pikalytics.com/results/naint19s",
                           "https://www.pikalytics.com/results/naint19j", "https://www.pikalytics.com/results/euint19m",
                           "https://www.pikalytics.com/results/euint19s", "https://www.pikalytics.com/results/euint19j",
                           "https://www.pikalytics.com/results/oceania19m", "https://www.pikalytics.com/results/oceania19s",
                           "https://www.pikalytics.com/results/oceania19j", "https://www.pikalytics.com/results/latamint19m",
                           "https://www.pikalytics.com/results/latamint19s", "https://www.pikalytics.com/results/latamint19j",
                           "https://www.pikalytics.com/results/pc2fin20", "https://www.pikalytics.com/results/pc2reg20",
                           "https://www.pikalytics.com/results/pcfin20", "https://www.pikalytics.com/results/oceania20m",
                           "https://www.pikalytics.com/results/oceania20s", "https://www.pikalytics.com/results/oceania20j",
                           "https://www.pikalytics.com/results/pc25inv21", "https://www.pikalytics.com/results/pc4fin21",
                           "https://www.pikalytics.com/results/pc4reg21", "https://www.pikalytics.com/results/pc3fin21",
                           "https://www.pikalytics.com/results/pc3reg21", "https://www.pikalytics.com/results/shefreg18m", "https://www.pikalytics.com/results/madreg18m",
                              "https://www.pikalytics.com/results/roanreg18m", "https://www.pikalytics.com/results/torreg18m",
                              "https://www.pikalytics.com/results/saltreg18m", "https://www.pikalytics.com/results/sindreg18m",
                              "https://www.pikalytics.com/results/portreg18m", "https://www.pikalytics.com/results/charreg18m",
                              "https://www.pikalytics.com/results/colinreg18m", "https://www.pikalytics.com/results/malmoreg18m",
                              "https://www.pikalytics.com/results/leipreg18m", "https://www.pikalytics.com/results/leipreg18s",
                              "https://www.pikalytics.com/results/leipreg18j", "https://www.pikalytics.com/results/dalreg18m",
                              "https://www.pikalytics.com/results/dalreg18s", "https://www.pikalytics.com/results/dalreg18j",
                              "https://www.pikalytics.com/results/madisonreg19m", "https://www.pikalytics.com/results/madisonreg19s",
                              "https://www.pikalytics.com/results/madisonreg19j", "https://www.pikalytics.com/results/santareg19m",
                              "https://www.pikalytics.com/results/santareg19s", "https://www.pikalytics.com/results/santareg19j",
                              "https://www.pikalytics.com/results/bristreg19m", "https://www.pikalytics.com/results/bristreg19s",
                              "https://www.pikalytics.com/results/bristreg19j", "https://www.pikalytics.com/results/hartreg19m",
                              "https://www.pikalytics.com/results/hartreg19s", "https://www.pikalytics.com/results/hartreg19j",
                              "https://www.pikalytics.com/results/daytonareg19m", "https://www.pikalytics.com/results/daytonareg19s",
                              "https://www.pikalytics.com/results/daytonareg19j", "https://www.pikalytics.com/results/greenreg19m",
                              "https://www.pikalytics.com/results/greenreg19j", "https://www.pikalytics.com/results/bramreg19m",
                              "https://www.pikalytics.com/results/bramreg19s", "https://www.pikalytics.com/results/bramreg19j",
                              "https://www.pikalytics.com/results/colreg19m", "https://www.pikalytics.com/results/colreg19s",
                              "https://www.pikalytics.com/results/colreg19j", "https://www.pikalytics.com/results/dalreg19m",
                              "https://www.pikalytics.com/results/dalreg19s", "https://www.pikalytics.com/results/dalreg19j",
                              "https://www.pikalytics.com/results/haroreg19m", "https://www.pikalytics.com/results/haroreg19s",
                              "https://www.pikalytics.com/results/haroreg19j", "https://www.pikalytics.com/results/anareg19m",
                              "https://www.pikalytics.com/results/anareg19s", "https://www.pikalytics.com/results/anareg19j",
                              "https://www.pikalytics.com/results/roreg19m", "https://www.pikalytics.com/results/roreg19s",
                              "https://www.pikalytics.com/results/roreg19j", "https://www.pikalytics.com/results/portreg19m",
                              "https://www.pikalytics.com/results/portreg19s", "https://www.pikalytics.com/results/portreg19j",
                              "https://www.pikalytics.com/results/memreg19m", "https://www.pikalytics.com/results/memreg19s",
                              "https://www.pikalytics.com/results/memreg19j", "https://www.pikalytics.com/results/frankreg19m",
                              "https://www.pikalytics.com/results/frankreg19s", "https://www.pikalytics.com/results/frankreg19j",
                              "https://www.pikalytics.com/results/philreg19m", "https://www.pikalytics.com/results/philreg19s",
                              "https://www.pikalytics.com/results/philreg19j", "https://www.pikalytics.com/results/pcinv20",
                              "https://www.pikalytics.com/results/malmoreg20m", "https://www.pikalytics.com/results/malmoreg20s",
                              "https://www.pikalytics.com/results/collinsvillereg20m", "https://www.pikalytics.com/results/collinsvillereg20s",
                              "https://www.pikalytics.com/results/collinsvillereg20j", "https://www.pikalytics.com/results/dallasreg20m",
                              "https://www.pikalytics.com/results/dallasreg20s", "https://www.pikalytics.com/results/dallasreg20j",
                              "https://www.pikalytics.com/results/bochumreg20m", "https://www.pikalytics.com/results/bochumreg20s",
                              "https://www.pikalytics.com/results/bochumreg20j"]



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


          mycursor.execute(sql, all_vals_p)

          mydb.commit()


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


          mycursor.execute(sql_teams, all_vals_team)

          mydb.commit()