import re
import pandas as pd

import mysql.connector
import mysql as mysql
import requests
import unidecode as unidecode
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)

from sqlalchemy import create_engine
engine = create_engine("mysql://"+"root"+":"+"Colormewild1!"+"@"+"localhost"+"/"+"pokemon_project")


#!pip install requests
#!pip install beautifulsoup4

import re
import requests
from bs4 import BeautifulSoup

#url = "https://www.pikalytics.com/results/pc2fin20"
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_name"

# def is_name_link(tag):
#     if tag is None or tag.parentElement is None:
#         return False
#     print(tag)
#     return (tag.parentElement.tagName == 'TD') and (tag.tagName == 'A')

page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")

name_links = soup.find_all('a')
name_links = [tag.attrs.get('href') for tag in name_links]
name_links = list(filter(None, name_links))

for i in range(len(name_links)):
    match_found = re.search('\/wiki\/.*_\(Pok%C3%A9mon\)', name_links[i])
    if match_found:
        name_links[i] = match_found.group(0)
    else:
        name_links[i] = None

name_links = list(filter(None, name_links))
# print(name_links)
# print(len(name_links))

# Every entry is duplicated due to the image links
end_of_list = name_links.index('/wiki/Zygarde_(Pok%C3%A9mon)') + 1
name_links = name_links[:end_of_list:2]
# Remove Pokemon not currently out in game yet
name_links.remove('/wiki/Basculegion_(Pok%C3%A9mon)')
name_links.remove('/wiki/Kleavor_(Pok%C3%A9mon)')
name_links.remove('/wiki/Wyrdeer_(Pok%C3%A9mon)')
print(name_links)

#### END OF FIRST BLOCK


import re
import requests
from bs4 import BeautifulSoup
import pprint

move_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_moves'
page = requests.get(move_url).text
soup = BeautifulSoup(page, "html.parser")

all_moves = []
rows = soup.find('table').find('table').find_all('tr')
for row in rows[1:-1]:
    cells = row.find_all('td')

    move_name = cells[1].find('a').text
    # Don't include Dynamax-specific moves
    if re.match('Max .*', move_name):
        continue

    move_type = cells[2].find('span').text
    move_category = cells[3].find('span').text

    pp = re.match('([0-9]{1,3})(\*)?(\\n)?', cells[5].text)
    move_pp = int(pp.group(1))

    power = re.match('([0-9]{1,3})(\*)?(\\n)?', cells[6].text)
    move_power = int(power.group(1)) if power else None

    acc = re.match('([0-9]{1,3})%', cells[7].text)
    move_accuracy = int(acc.group(1)) if acc else None

    if len(all_moves) > 0 and all_moves[-1][0] == move_name:
        all_moves.pop(-1)
    else:
        all_moves.append([move_name, move_type, move_category, move_pp, move_power, move_accuracy])


### END OF SECOND BLOCK


import re
import requests
import pprint as pp
from bs4 import BeautifulSoup

# test_url = 'https://bulbapedia.bulbagarden.net/wiki/Calyrex_(Pok%C3%A9mon)'
# test_url = 'https://bulbapedia.bulbagarden.net/wiki/Togetic_(Pok%C3%A9mon)'
# test_url = 'https://bulbapedia.bulbagarden.net/wiki/Whirlipede_(Pok%C3%A9mon)'
# test_url = 'https://bulbapedia.bulbagarden.net/wiki/Chinchou_(Pok%C3%A9mon)'

roman_num = {'I': 1,
             'II': 2,
             'III': 3,
             'IV': 4,
             'V': 5,
             'VI': 6,
             'VII': 7,
             'VIII': 8}

# Start with this one since no Pokemon has it
all_abilities = ['Cacophony']
species_dict = {}
learns_move = []
# for link in ['/wiki/Rattata_(Pok%C3%A9mon)', '/wiki/Raticate_(Pok%C3%A9mon)', '/wiki/Geodude_(Pok%C3%A9mon)', '/wiki/Graveler_(Pok%C3%A9mon)', '/wiki/Golem_(Pok%C3%A9mon)', '/wiki/Grimer_(Pok%C3%A9mon)', '/wiki/Muk_(Pok%C3%A9mon)']:
#for link in ['/wiki/Kyogre_(Pok%C3%A9mon)', '/wiki/Rillaboom_(Pok%C3%A9mon)', '/wiki/Tornadus_(Pok%C3%A9mon)', '/wiki/Tsareena_(Pok%C3%A9mon)', '/wiki/Urshifu_(Pok%C3%A9mon)', '/wiki/Weavile_(Pok%C3%A9mon)', '/wiki/Arcanine_(Pok%C3%A9mon)', '/wiki/Calyrex_(Pok%C3%A9mon)', '/wiki/Indeedee_(Pok%C3%A9mon)', '/wiki/Mienshao_(Pok%C3%A9mon)', '/wiki/Stakataka_(Pok%C3%A9mon)', '/wiki/Whimsicott_(Pok%C3%A9mon)', '/wiki/Amoonguss_(Pok%C3%A9mon)', '/wiki/Incineroar_(Pok%C3%A9mon)', '/wiki/Volcarona_(Pok%C3%A9mon)', '/wiki/Xerneas_(Pok%C3%A9mon)', '/wiki/Nihilego_(Pok%C3%A9mon)', '/wiki/Regieleki_(Pok%C3%A9mon)', '/wiki/Cherrim_(Pok%C3%A9mon)', '/wiki/Dusclops_(Pok%C3%A9mon)', '/wiki/Entei_(Pok%C3%A9mon)', '/wiki/Groudon_(Pok%C3%A9mon)', '/wiki/Zapdos_(Pok%C3%A9mon)', '/wiki/Grimmsnarl_(Pok%C3%A9mon)', '/wiki/Zacian_(Pok%C3%A9mon)', '/wiki/Dragonite_(Pok%C3%A9mon)', '/wiki/Krookodile_(Pok%C3%A9mon)', '/wiki/Torkoal_(Pok%C3%A9mon)', '/wiki/Landorus_(Pok%C3%A9mon)', '/wiki/Tapu_Fini_(Pok%C3%A9mon)']:
# for link in ['/wiki/Nidoran%E2%99%82_(Pok%C3%A9mon)', '/wiki/Nidoran%E2%99%80_(Pok%C3%A9mon)', '/wiki/Farfetch%27d_(Pok%C3%A9mon)', '/wiki/Sirfetch%27d_(Pok%C3%A9mon)', '/wiki/Type:_Null_(Pok%C3%A9mon)']:
#for link in name_links[name_links.index('/wiki/Groudon_(Pok%C3%A9mon)'):]:
#for link in name_links[600:605]:
for link in name_links:
    name = re.match('\/wiki\/(.*)_\(Pok%C3%A9mon\)', link).group(1)
    url = 'https://bulbapedia.bulbagarden.net' + link
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")


    # print("first url", url)
    # -------Abilities-----------

    # I think this is the only invalid case, but I'm not entirely sure, so I made it a list
    def not_invalid(href):
        return href not in ['/wiki/Cacophony_(Ability)']


    # Plural vs. singular for abilit(y)(ies)
    main_table = soup.find("span", text='Abilities').find_parent('table') if soup.find("span",
                                                                                       text='Abilities') else soup.find(
        "span", text='Ability').find_parent('table')

    links = [tag.attrs.get('href') for tag in main_table.find_all('a', {'href': re.compile('\/wiki\/.*_\(Ability\)')})]
    abilities = set(filter(not_invalid, links))
    abilities = [re.match('\/wiki\/(.*)_\(Ability\)', link).group(1).replace('%27', '\'').replace('_', ' ') for link in
                 abilities]

    # -------Generation---------
    gen = soup.find(string=re.compile('Generation ([IV]{1,4})'))
    gen = re.search('Generation ([IV]{1,4})', gen).group(1)
    gen = roman_num[gen]

    # -------Evolution----------
    # Pokemon who don't have the word 'evolve' as a link for some reason
    if name not in ['Eternatus']:
        evo_paragraph = soup.find(title='Evolution').find_parent('p').text
        fully_evolved = False if re.search('.* evolves into .*', evo_paragraph) else True
    else:
        fully_evolved = True

    # Build a list of all distinct names of abilities
    for ability in abilities:
        if ability not in all_abilities:
            all_abilities.append(ability)

    # -------Base stats---------
    # hp = soup.find(href = '/wiki/HP').parent.findNext('div').text
    # attack = soup.find(href = '/wiki/Stat#Attack').parent.findNext('div').text
    # defense = soup.find(href = '/wiki/Stat#Defense').parent.findNext('div').text
    # spAtk = soup.find(href = '/wiki/Stat#Special_Attack').parent.findNext('div').text
    # spDef = soup.find(href = '/wiki/Stat#Special_Defense').parent.findNext('div').text
    # speed = soup.find(href = '/wiki/Stat#Speed').parent.findNext('div').text

    start = soup.find(id='Base_stats')
    if not start:
        start = soup.find(id='Stats')
    start_set = start.find_all_next(href='/wiki/HP')
    end = soup.find(id='Type_effectiveness')
    end_set = end.find_all_previous(href='/wiki/HP')

    hp_links = [link for link in start_set if link in end_set]

    for i in range(len(hp_links)):

        table = hp_links[i].find_parent('table')

        atk_link = table.find(href='/wiki/Stat#Attack')
        defense_link = table.find(href='/wiki/Stat#Defense')
        sp_atk_link = table.find(href='/wiki/Stat#Special_Attack')
        sp_def_link = table.find(href='/wiki/Stat#Special_Defense')
        speed_link = table.find(href='/wiki/Stat#Speed')

        form_name = ''
        qualified_name = name
        if len(hp_links) > 1:
            form_name = table.find_previous_sibling(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']).text

            # Check if Pokemon has multiple tables representing base stat
            # changes in different generations. If so, take only the most recent
            valid_gen_regex = 'Generation [IV]{1,4} onward'
            matches_valid_gen_regex = re.match(valid_gen_regex, form_name)
            invalid_gen_regex = 'Generation[s]? [IV]{1,4}(-[IV]{1,4})?'
            matches_invalid_gen_regex = re.match(invalid_gen_regex, form_name)
            if matches_invalid_gen_regex and not matches_valid_gen_regex:
                continue
            elif matches_valid_gen_regex:
                form_name = ''

            # print(name)

            regex = '(.*)' + name + '(.*)'
            xyregex = '(Mega) ' + name + ' ([XY])'

            # Basically, if the form name is present in the form name anywhere,
            # it gets removed (along with leading/trailing spaces/hyphens)
            # These try/except blocks are to make these lines "optional"
            try:
                temp = re.match(xyregex, form_name)
                form_name = temp.group(1).strip(' -') + ' ' + temp.group(2).strip(' -')
            except:
                pass

            try:
                form_name = re.match(regex, form_name).group(1).strip(' -')
            except:
                pass

            try:
                form_name = re.match(regex, form_name).group(2).strip(' -')
            except:
                pass

            if form_name == '' or form_name.upper() == 'Base stats'.upper() or form_name == ' ':
                form_name = ''
                qualified_name = name
            else:
                qualified_name = name + ' (' + form_name + ')'

        print(qualified_name)

        hp = hp_links[i].parent.findNext('div').text
        attack = atk_link.parent.findNext('div').text
        defense = defense_link.parent.findNext('div').text
        sp_atk = sp_atk_link.parent.findNext('div').text
        sp_def = sp_def_link.parent.findNext('div').text
        speed = speed_link.parent.findNext('div').text

        # -------Types-------
        # type_links = soup.find(href='/wiki/Type').find_parent('b').find_next('table').find_all(href = re.compile('\/wiki\/(.*)_\(Type\)'))
        # type_cells = soup.find(href='/wiki/Type').find_parent('b').find_next('table').find_all(lambda tag : (tag.name == 'td') and not (tag.find('td') and not (tag.attrs['href'] == '/wiki/Unknown_(type)' if tag.attrs.get('href') else True)))
        # print("soupsoupsoup\n", soup.find(href='/wiki/Type').find_parent(True))
        # print("soup url", url)
        # print(soup.find('table').find_next('table'))

        # type_cells = soup.find(href='/wiki/Type').find_parent('b').find_next('table').find_all(lambda tag : (tag.name == 'td') and not tag.find(href = '/wiki/Unknown_(type)'))
        smalls = soup.find(href='/wiki/Type').find_parent('b').find_next('table').find_all(
            lambda tag: (tag.name == 'small') and not tag.text == '')
        type_cells = {small.text: small.find_previous_sibling('table').find_all(
            lambda tag: (tag.name == 'td') and not tag.find(href='/wiki/Unknown_(type)')) for small in smalls}
        # -------
        # print(type_cells)
        type1 = 'N/A'
        type2 = 'N/A'
        # There's more than one form, so need to get the types from the right one
        form_check_regex = '(.*)' + form_name + '(.*)'
        print(form_name)
        # print(form_check_regex)
        # print(type_cells)
        # print("len ", len(type_cells))
        # There will always be at least one of these cells
        # print("type cells", type_cells)
        # Inconsistencies abound--I have to make these exceptions
        if name == 'Zygarde':
            type_cells['50% Forme'] = []
        if name == 'Indeedee':
            type1 = 'Psychic'
            type2 = 'Normal'
        if name == 'Aegislash':
            type1 = 'Steel'
            type2 = 'Ghost'
        if name == 'Lycanroc':
            type1 = 'Rock'
        if name == 'Pumpkaboo':
            type1 = 'Ghost'
            type2 = 'Grass'
        if not type_cells:
            type_cells = {'pass': 'pass'}
        for key in type_cells:
            try:
                # print("goes here")
                # If there's more than one form, we need to get the types from the right one
                # form = type_cells[j].find('small').text
                # print("mmmmm", form)
                # print("one")
                if re.match(form_check_regex, key):
                    # print("two")
                    # type_texts = [type_cells[key][0].find('b'), type_cells[key][1].find('b')]
                    # print("three")
                    # Remove newline character at the end
                    type1 = type_cells[key][0].text.split('\n')[0]
                    # print("four")
                    if len(type_cells[key]) == 2:
                        # print("five")
                        type2 = type_cells[key][1].text.split('\n')[0]
                    break
            # Will enter this except block when there's no form name underneath the type
            # (There are some extra cells that get brought in from the scraping, for some reason, so
            # this conditional is a way of dealing with that)
            except:
                # print("then here")
                print("in except ", name)
                # print("llllllllllllll", form_name)
                # if form_name == '' or (j == len(type_cells[key]) - 1):
                # if form_name == '':
                # type_texts = type_cells[key][0].find('b')
                # print("asdflkjasdflkj", type_texts)
                temp_table = soup.find(href='/wiki/Type').find_parent('b').find_next(
                    'table')  # .find_all(lambda tag : (tag.name == 'td') and not tag.find('td'))
                types = list(filter(lambda _type: _type != 'Unknown', [b.text for b in temp_table.find_all('b')]))
                type1 = types[0]
                if len(types) == 2:
                    type2 = types[1]
                # break
                # else:
                #     continue

        # -----Moves--------
        # These Pokemon have certain forms available in Gen 8 and others not, so we'll just
        # take a shortcut and only pull from their gen 7 learnset
        alolan_forms = ['Rattata', 'Raticate', 'Geodude', 'Graveler', 'Golem',
                        'Grimer', 'Muk']
        if soup.find(text=re.compile('This Pokémon is unavailable within')) or name in alolan_forms:
            url += '/Generation_VII_learnset'
            print('url\n', url)
            page = requests.get(url).text
            soup = BeautifulSoup(page, "html.parser")

        ##########################################################
        learnset = set()
        # TODO need to add the Pokemon here that have stat differences across generations since
        # they have multiple tables...at least, I think that's why it happens. Might need to just run
        # this a bunch and add anything that fails into this list...
        pkmn_without_learnset_diffs = ['Pumpkaboo', 'Gourgeist', 'Giratina', 'Basculin',
                                       'Landorus', 'Thundurus', 'Tornadus', 'Rotom', 'Meloetta', 'Greninja',
                                       'Aegislash', 'Zygarde', 'Wishiwashi', 'Minior', 'Necrozma', 'Eiscue', 'Zacian',
                                       'Zamazenta',
                                       'Eternatus', 'Kyogre', 'Groudon', 'Qwilfish', 'Pikachu', 'Gardevoir',
                                       'Kangaskhan', 'Venusaur',
                                       'Charizard', 'Blastoise', 'Alakazam', 'Gengar', 'Pinsir', 'Gyarados',
                                       'Aerodactyl', 'Mewtwo',
                                       'Ampharos', 'Scizor', 'Heracross', 'Houndoom', 'Tyranitar', 'Blaziken', 'Mawile',
                                       'Aggron',
                                       'Medicham', 'Manectric', 'Banette', 'Absol', 'Latias', 'Latios', 'Garchomp',
                                       'Lucario', 'Abomasnow',
                                       'Beedrill', 'Pidgeot', 'Slowbro', 'Steelix', 'Sceptile', 'Swampert', 'Sableye',
                                       'Sharpedo', 'Camerupt',
                                       'Altaria', 'Glalie', 'Salamence', 'Metagross', 'Rayquaza', 'Lopunny', 'Gallade',
                                       'Audino', 'Diancie', 'Psyduck',
                                       'Roserade', 'Scolipede', 'Seismitoad', 'Solrock', 'Stoutland', 'Vileplume',
                                       'Wigglytuff', 'Azumarill',
                                       'Beartic', 'Bellossom', 'Butterfree', 'Clefable', 'Crustle', 'Cryogonal',
                                       'Darmanitan', 'Eevee',
                                       'Exploud', 'Gigalith', 'Jumpluff', 'Krookodile', 'Lunatone', 'Mantine', 'Minior',
                                       'Nidoking', 'Nidoqueen',
                                       'Noctowl', 'Pelipper', 'Poliwrath', 'Illumise', 'Arbok', 'Ariados', 'Beautifly',
                                       'Chimecho', 'Delcatty',
                                       'Dodrio', 'Electrode', 'Magcargo', 'Shaymin', 'Volbeat', 'Kyurem', 'Leavanny',
                                       'Masquerain', 'Staraptor',
                                       'Swellow', 'Unfezant', 'Victreebel', 'Woobat', 'Unown']
        if len(hp_links) > 1 and name not in pkmn_without_learnset_diffs:
            # Level up
            form_cursor = soup.find(id='Learnset')
            if not form_cursor:
                form_cursor = soup.find(id='By_leveling_up')
            temp = form_cursor.find_next(text=(form_name + ' ' + name if form_name != '' else name))
            # print("temp ", temp)
            if not temp:
                # print("not temp\n")
                temp = form_cursor.find_next(text=form_name)
            form_cursor = temp

            table_rows = form_cursor.find_next('table').find('tr').find_next_sibling('tr').find_all('tr')
            # print("form cursor\n", form_cursor)
            # print("table rows\n", table_rows)
            for row in table_rows[1:]:
                move_name = row.find_all('td')[1].find('a').text
                learnset.add(move_name)

            try:
                # TM/TR
                temp = form_cursor.find_next('span', text=(form_name + ' ' + name if form_name != '' else name))
                if not temp:
                    temp = form_cursor.find_next('span', text=form_name)
                form_cursor = temp
                # print('in TM: ', form_name, 'form_cursor: ', form_cursor)
                table_rows = form_cursor.find_next('table').find('tr').find_next_sibling('tr').find_all('tr')
                for row in table_rows[1:]:
                    move_name = row.find_all('td')[2].find('a').text
                    learnset.add(move_name)
            except:
                pass

            try:
                # Breeding
                temp = form_cursor.find_next('span', text=(form_name + ' ' + name if form_name != '' else name))
                if not temp:
                    temp = form_cursor.find_next('span', text=form_name)
                form_cursor = temp
                table_rows = form_cursor.find_next('table').find('tr').find_next_sibling('tr').find_all('tr')
                for row in table_rows[1:]:
                    move_name = row.find_all('td')[1].find('a').text
                    learnset.add(move_name)
            except:
                pass

            try:
                # Tutoring
                temp = form_cursor.find_next('span', text=(form_name + ' ' + name if form_name != '' else name))
                if not temp:
                    temp = form_cursor.find_next('span', text=form_name)
                form_cursor = temp
                table_rows = form_cursor.find_next('table').find('tr').find_next_sibling('tr').find_all('tr')
                for row in table_rows[1:]:
                    move_name = row.find_all('td')[0].find('a').text
                    learnset.add(move_name)
            except:
                pass

            try:
                # Form Change
                temp = form_cursor.find_next('span', text=(form_name + ' ' + name if form_name != '' else name))
                if not temp:
                    temp = form_cursor.find_next('span', text=form_name)
                form_cursor = temp
                table_rows = form_cursor.find_next('table').find('tr').find_next_sibling('tr').find_all('tr')
                for row in table_rows[1:]:
                    move_name = row.find_all('td')[1].find('a').text
                    learnset.add(move_name)
            except:
                pass

            new_learnset = set()
            # print('all moves\n', all_moves)
            for move in learnset:
                # Get rid of extraneous strings from the learnset
                # (sometimes things like type names would end up in it for some reason)
                # print(move)
                if move in [move[0] for move in all_moves]:
                    new_learnset.add(move)
            # print("new learnset\n")
            # pp.pprint(new_learnset)
            learnset = new_learnset

        # Pokemon has no form differences
        else:
            start = soup.find(id='Learnset')
            if not start:
                start = soup.find(id='By_leveling_up')
            end = soup.find(id='TCG-only_moves')
            if not end:
                end = soup.find(id='Anime-only_moves')
            if not end:
                end = soup.find(id='Side_game_data')
            if not end:
                end = soup.find(title='Special:Categories')
            # print('end: ', end)
            # links = start.find_all_next('a')
            start_set = start.find_all_next('a')
            end_set = end.find_all_previous('a')

            links = [linkx for linkx in start_set if linkx in end_set]

            # print("links\n", links)
            for move in all_moves:
                for linky in links:
                    if linky.text == move[0]:
                        learnset.add(move[0])

        if name == 'Unown':
            learnset = set({'Hidden Power'})

        # Name fixes for special symbols
        if name == 'Nidoran%E2%99%82':
            name = 'Nidoran'
            qualified_name = 'Nidoran (Male)'
        if name == 'Nidoran%E2%99%80':
            name = 'Nidoran'
            qualified_name = 'Nidoran (Female)'
        if name == 'Farfetch%27d':
            name = 'Farfetch\'d'
            qualified_name = 'Farfetch\'d (Galarian)' if form_name != '' else 'Farfetch\'d'
        if name == 'Sirfetch%27d':
            name = 'Sirfetch\'d'
            qualified_name = name
        # if name == 'Type:_Null':
        #     name = 'Type: Null'
        #     qualified_name = name
        space_name = re.match("(.*)_(.*)", name)
        if space_name:
            name = space_name.group(1) + " " + space_name.group(2)
            qualified_name = name

        for move in learnset:
            learns_move.append([qualified_name, move])

        pp.pprint(learnset)
        # print(learns_move)

        if form_name == 'Alolan':
            gen = 7
        elif form_name == 'Galarian':
            gen = 8
        elif qualified_name == 'Rotom (Heat, Wash, Frost, Fan, and Mow)':
            # It's a lot easier/faster just to hard-code these than split up the string and grab all the form names with regex
            species_dict['Rotom-Heat'] = ['Electric', 'Fire', hp, attack, defense, sp_atk, sp_def, speed, abilities,
                                          gen, fully_evolved]
            species_dict['Rotom-Wash'] = ['Electric', 'Water', hp, attack, defense, sp_atk, sp_def, speed, abilities,
                                          gen, fully_evolved]
            species_dict['Rotom-Frost'] = ['Electric', 'Ice', hp, attack, defense, sp_atk, sp_def, speed, abilities,
                                           gen, fully_evolved]
            species_dict['Rotom-Fan'] = ['Electric', 'Flying', hp, attack, defense, sp_atk, sp_def, speed, abilities,
                                         gen, fully_evolved]
            species_dict['Rotom-Mow'] = ['Electric', 'Grass', hp, attack, defense, sp_atk, sp_def, speed, abilities,
                                         gen, fully_evolved]
            continue

        species_dict[qualified_name] = [type1, type2, hp, attack, defense, sp_atk, sp_def, speed, abilities, gen,
                                        fully_evolved]

        # print(f'form name: {form_name}\n')
        # print(f'qualified name: {qualified_name}\n')
        # print(f'HP: {hp}\nAtk: {attack}\nDef: {defense}\nSpAtk: {sp_atk}\nSpDef: {sp_def}\nSpeed: {speed}\n')

        # If the url changed due to going to a different (learnset) page, change it back on new iteration
        print("link\n", link)
        url = 'https://bulbapedia.bulbagarden.net' + link
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")

    # print(name)
    # print(gen)
    # print("Fully evolved: " + str(fully_evolved))
    # print(abilities)
    # print("HP: " + hp + "\n" + "Atk: " + attack + "\n" + "Def: " + defense + "\n" + "SpAtk: " + spAtk + "\n" + "SpDef: " + spDef + "\n" + "Speed: " + speed + "\n")

pp.pprint(species_dict)
print(sorted(all_abilities))

# TODO check these
# for species in species_dict:
#     type1 = species_dict[species][0]
#     type2 = species_dict[species][1]
#     if type1 == 'N/A' and type2 == 'N/A':
#         print("typeless: ", name)

# TODO write these to tables:
# all_abilities
# all_moves
# learns_move
# species_dict -- need to unwind/normalize this because of the abilities list
# TODO make a new list called has_ability?

# TODO I don't think it's possible to programmatically separate out the abilities for the different forms due to
# how they're notated in different ways for the different species--update: might be able to do the same thing
# I do for types to do this


# TODO it looks like we'll have to do some rule-checking for each Pokemon that we find on Pikalytics
# Example: find Landorus--check if it's in dict of Pokemon with form differences--if so (yes),
# get function stored as value in dict, pass in all details of the Pokemon to function--
# function should return the form name (or entire name with form included)

# TODO note: there is at least one case where the ability is misspelled on Pikalytics--Alolan Raichu's
# "Surge Surfer" became "Surge Surger"--need to catch those--also, this is the condition for Alolan Raichu

### END OF THIRD BLOCK


import pandas as pd
# TODO remember that Aegislash is split into two entries, so need to account for that in the SQL queries
#print(species_dict)
has_ability = []
for species in species_dict:
    species_abilities = species_dict[species].pop(8)
    #print(species_abilities)
    for sp_ability in species_abilities:
        has_ability.append([species, sp_ability])

has_ability_df = pd.DataFrame(has_ability, columns=["species_name", "ability_name"])
#has_ability_df

species_df = pd.DataFrame.from_dict(species_dict, orient='index', columns=["species_type_1", "species_type_2", "base_hp", "base_atk", "base_def", "base_spAtk", "base_spDef", "base_speed", "gen_of_origin", "is_fully_evolved"])
species_df.index.name = "species_name"
#species_df

learns_move_df = pd.DataFrame(learns_move, columns=["species_name", "move_name"])
#learns_move_df

moves_df = pd.DataFrame(all_moves, columns=["move_name", "move_type", "move_category", "power_points", "power", "accuracy"])
#moves_df

abilities_df = pd.DataFrame(all_abilities, columns=["ability_name"])



# END OF FOURTH BLOCK


# Connection info for the database
mydb = mysql.connector.connect(

         host="localhost",
         user="root",

         ## Should do the password-hiding thing shown in the slides (??)
         password="Colormewild1!",

         database="pokemon_project"

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
        # no_comma = no_quotation.capitalize().replace(",", "")
        no_comma = no_quotation.title().replace(",", "")

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
#print("pokemon_list\n", pokemon_list)
for item in str(pokemon_list).split("]"):
    if "moves" in str(item):
        list = []
        #print("first character: ", item.split("moves")[1][1])
        list.append(item.split("moves")[1])
        pokemon_list_moves.append(list)

#print(pokemon_list_moves)

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

    regex = "(.*)-[Gg]max"

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


#print("data_list", data_list)
df = pd.DataFrame(data_list, columns=['team_id', 'pokemon_id'])


# Updating the team id
i = 0
for team_id in team_ids:

         df.at[i, "team_id"] = team_id
         i = i + 1





# insert the dataframe into a table
df.to_sql("team_members", engine, if_exists="replace")


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

#print("data_list_all_pokemon", data_list_all_pokemon)
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

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@




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

print(moves_ids_list)

single_move = []
l = 0
for item in str(pokemon_list_moves).split("}"):
    single_move_clean = str(item).replace("]]", "")
    single_move_clean2 = single_move_clean.replace("\"", "")
    single_move_clean3 = single_move_clean2.replace("{name:", "")

    regex2 = "(.*),type:"
    regex3 = "([A-Z, a-z]*)"

    match = re.match(regex2, single_move_clean3)


    if match:

        single_move_clean4 = match.group(1)
        single_move_clean5 = single_move_clean4.replace(":", "")
        single_move_clean6 = single_move_clean5.replace(",", "")
        single_move_clean7 = single_move_clean6.replace("[", "")
        single_move_clean8 = single_move_clean7.replace("]", "")
        single_move_clean9 = single_move_clean8.replace("'", "")

        single_move.append(single_move_clean9)







#make dataframe for HasMove
data_list_hasMove = []
for item in moves_ids_list:

    frame_row = [item, "0"]



    data_list_hasMove.append(frame_row)

df_hasMove = pd.DataFrame(data_list_hasMove, columns=['pokemon_id', 'move_name'])

for i in range(len(single_move)):
    single_move[i] = single_move[i].strip()

# updating the moves
i = 0
for single in single_move:


    df_hasMove.at[i, "move_name"] = single
    i = i + 1


#print(df_hasMove)

#insert the pokemon datafram into a table
#df_hasMove.to_sql("has_move", engine, if_exists="replace")

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# it goes between code where Pokemon instance dictionary is made and dataframe is made from said dictionary
form_checker = {
    "Aegislash": lambda name, ability, moves, item: "Aegislash (Shield Forme)",
    "Groudon": lambda name, ability, moves, item: "Groudon (Primal)" if item == "Red Orb" else "Groudon",
    "Kyogre": lambda name, ability, moves, item: "Kyogre (Primal)" if item == "Blue Orb" else "Kyogre",
    "Giratina": lambda name, ability, moves, item: "Giratina (Origin Forme)" if item == "Griseous Orb" else "Giratina (Altered Forme)",
    "Giratina-Origin": lambda name, ability, moves, item: "Giratina (Origin Forme)",
    "Landorus": lambda name, ability, moves,
                       item: "Landorus (Therian Forme)" if ability == "Intimidate" else "Landorus (Incarnate Forme)",
    "Thundurus": lambda name, ability, moves,
                        item: "Thundurus (Therian Forme)" if ability == "Volt Absorb" else "Thundurus (Incarnate Forme)",
    "Tornadus": lambda name, ability, moves,
                       item: "Tornadus (Therian Forme)" if ability == "Regenerator" else "Tornadus (Incarnate Forme)",
    "Kyurem": lambda name, ability, moves, item: "Kyurem (White)" if ability == "Turboblaze" else (
        "Kyurem (Black)" if ability == "Teravolt" else "Kyurem"),
    "Kyurem-White": lambda name, ability, moves, item: "Kyurem (White)",
    "Kyurem-Black": lambda name, ability, moves, item: "Kyurem (Black)",
    "Greninja": lambda name, ability, moves, item: "Greninja (Ash)" if ability == "Battle Bond" else "Greninja",
    "Zygarde": lambda name, ability, moves,
                      item: "Zygarde (Complete Forme)" if ability == "Power Construct" else "Zygarde",
    "Zygarde-10%": lambda name, ability, moves, item: "Zygarde (10% Forme)",
    "Necrozma": lambda name, ability, moves, item: "Necrozma (Dawn Wings)" if "Moongeist Beam" in moves else (
        "Necrozma (Dusk Mane)" if "Sunsteel Strike" in moves else "Necrozma"),
    "Necrozma-Dawn-Wings": lambda name, ability, moves, item: "Necrozma (Dawn Wings)",
    "Necrozma-Dusk-Mane": lambda name, ability, moves, item: "Necrozma (Dusk Mane)",
    "Zacian": lambda name, ability, moves,
                     item: "Zacian (Crowned Sword)" if item == "Rusted Sword" else "Zacian (Hero of Many Battles)",
    "Zamazenta": lambda name, ability, moves,
                        item: "Zamazenta (Crowned Shield)" if item == "Rusted Shield" else "Zamazenta (Hero of Many Battles)",
    "Urshifu": lambda name, ability, moves,
                      item: "Urshifu (Rapid Strike Style)" if "Surging Strikes" in moves else "Urshifu (Single Strike Style)",
    "Calyrex": lambda name, ability, moves, item: "Calyrex (Shadow Rider)" if "Astral Barrage" in moves else (
        "Calyrex (Ice Rider)" if "Glacial Lance" in moves else "Calyrex"),
    "Ninetales": lambda name, ability, moves,
                        item: "Ninetales (Alolan)" if ability == "Snow Cloak" or ability == "Snow Warning" else "Ninetales",
    "Sandslash": lambda name, ability, moves,
                        item: "Sandslash (Alolan)" if ability == "Snow Cloak" or ability == "Slush Rush" else "Sandslash",
    "Raichu": lambda name, ability, moves,
                     item: "Raichu (Alolan)" if ability == "Surge Surfer" or ability == "Surge Surger" else "Raichu",
    "Persian": lambda name, ability, moves,
                      item: "Persian (Alolan)" if ability == "Fur Coat" or ability == "Rattled" else "Persian",
    "Indeedee": lambda name, ability, moves, item: "Indeedee (Female)"

}
# assuming that there's a dict called poke_dict holding all the individual Pokemon that maps pokemon_id : [attributes]
# attributes in order: species_name, [species_type (type1, type2)], ability, [moves (4)], held_item, can_gmax
# for poke_id in poke_dict:
#     name = poke_dict[poke_id][0]
#     types = poke_dict[poke_id][1]
#     ability = poke_dict[poke_id][2]
#     moves = poke_dict[poke_id][3]
#     item = poke_dict[poke_id][4]
#     # Change the name depending on what form it is. Ex. Calyrex that knows Astral Barrage => Calyrex (Shadow Rider)
#     if (name in form_checker):
#         poke_dict[poke_id][0] = form_checker[name](name, types, ability, moves, item)
#     else:
#         # If Pokemon is holding a mega stone, treat it as its mega form
#         poke_dict[poke_id][0] = name + ' (Mega)' if re.match("(.*)ite(.*)", item) else name

# print(poke_dict)
#print("single_move", single_move)

#print("single_move", single_move)

move_index_list = [[moves_ids_list[i], single_move[i]] for i in
                   range(len(moves_ids_list))]  # moves_ids_list, single_move

for index, row in df_all_pokemon.iterrows():
    name = df_all_pokemon.at[index, "species_name"]
    ability = df_all_pokemon.at[index, "ability"]
    moves = [item[1] for item in move_index_list if item[0] == index]

    print(name, " ", moves, "\n")

    item = df_all_pokemon.at[index, "item"]
    # Change the name depending on what form it is. Ex. Calyrex that knows Astral Barrage => Calyrex (Shadow Rider)
    if (name in form_checker):
        df_all_pokemon.at[index, "species_name"] = form_checker[name](name, ability, moves, item)
    else:
        # If Pokemon is holding a mega stone, treat it as its mega form
        df_all_pokemon.at[index, "species_name"] = name + ' (Mega)' if re.match("^(?!([Ee]violite)$).*ite$", item) else name



print("Has ability df:")
print(has_ability_df)

print("species df:")
print(species_df)

print("learns move df:")
print(learns_move_df)

print("all pokemon df:")
print(df_all_pokemon)


#%%%%%%%%%%%%%%%%% Getting info for Trainer, Tournament, Competes, Team

trainer_names = []
trainer_nationalities = []
trainer_dictionary = {}

# Getting the names and nationalities from pages formatted like "trainer name (trainer nationality)"


urls_with_nationalities = ["https://www.pikalytics.com/results/worlds18m", "https://www.pikalytics.com/results/worlds18s",
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
                           "https://www.pikalytics.com/results/pc3reg21"]



urls_without_nationalities = ["https://www.pikalytics.com/results/shefreg18m", "https://www.pikalytics.com/results/madreg18m",
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


for url in urls_with_nationalities:

     page = requests.get(url).text
     soup = BeautifulSoup(page, "html.parser")

     trainer_links = soup.find_all("h2")


     for trainer in trainer_links:

         trainer_names_string = unidecode.unidecode(trainer.text)

         trainer_names_sub = unidecode.unidecode(re.sub(r'\([^)]*\)', '', trainer_names_string))


         trainer_names.append(trainer_names_sub)

         trainer_nationalities_string = trainer_names_string[trainer_names_string.find("(")+1:trainer_names_string.find(")")]

         trainer_nationalities.append(trainer_nationalities_string)

         trainer_dictionary[unidecode.unidecode(trainer_names_sub)] = trainer_nationalities_string


# Getting the trainer names from results pages formatted like "trainer name"
for url in urls_without_nationalities:

      page = requests.get(url).text
      soup = BeautifulSoup(page, "html.parser")

      trainer_links = soup.find_all("h2")



      for trainer in trainer_links:

          trainer_names_string = unidecode.unidecode(trainer.text)
          trainer_names_sub = re.sub(r'\([^)]*\)', '', trainer_names_string)

          trainer_names.append(unidecode.unidecode(trainer_names_sub))

          trainer_nationalities_string = trainer_names_string[trainer_names_string.find("(")+1:trainer_names_string.find(")")]

          trainer_nationalities.append(trainer_nationalities_string)


          if trainer_names_string[0] == trainer_nationalities_string[0] \
                  and trainer_names_string[1] == trainer_nationalities_string[1] \
                  and trainer_names_string[2] == trainer_nationalities_string[2]:

              trainer_dictionary[trainer_names_sub] = "none"

#print(trainer_dictionary)


# removing the duplicate key/value pairs from the trainer dictionary
temp = []
res = dict()
for key, val in trainer_dictionary.items():



    if key not in temp:
        temp.append(key)
        res[key] = val


# Getting the tournament info for the tournament table


tournament_dictionary = {}

for url in urls_with_nationalities:

    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    tournament_title = soup.select("h1")[0].text.strip()

    if len(tournament_title.split(" ")[0]) == 7:
        tournament_year = tournament_title.split(" ")[0].replace("VGC", "")

    if len(tournament_title.split(" ")[1]) == 4:
        tournament_year = tournament_title.split(" ")[1]

    if len(tournament_title.split(" ")[1]) == 2:
        tournament_year = "20" + tournament_title.split(" ")[1]

    #tournament_year = str(tournament_title).split(" ")[0].replace("VGC", "")

    tournament_dictionary[tournament_title] = tournament_year

for url in urls_without_nationalities:
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    tournament_title = soup.select("h1")[0].text.strip()


    if len(tournament_title.split(" ")[0]) == 7:
        tournament_year = tournament_title.split(" ")[0].replace("VGC", "")

    if len(tournament_title.split(" ")[1]) == 4:
        tournament_year = tournament_title.split(" ")[1]

    if len(tournament_title.split(" ")[1]) == 2:
        tournament_year = "20" + tournament_title.split(" ")[1]

    #tournament_year = "20" + str(tournament_title).split(" ")[1]

    tournament_dictionary[tournament_title] = tournament_year


# Getting the placement info for the Placement table

# placement results that include nationality
placement_urls_with_natl = ["https://www.pikalytics.com/results/worlds18m", "https://www.pikalytics.com/results/worlds18s",
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
                           "https://www.pikalytics.com/results/pc3reg21"]




placement_dictionary = {}

# Gets Placement table info from those events that include nationality
for url in placement_urls_with_natl:

    #tournament_dictionary_placement = {}
    #tournament_dictionary_placement['VGC2019 North American Juniors Internationals'] = "2019"

    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    tournament_title_placement = soup.select("h1")[0].text.strip()

    if len(tournament_title_placement.split(" ")[0]) == 7:
        tournament_year_placement = tournament_title_placement.split(" ")[0].replace("VGC", "")

    if len(tournament_title_placement.split(" ")[1]) == 4:
        tournament_year_placement = tournament_title_placement.split(" ")[1]

    if len(tournament_title_placement.split(" ")[1]) == 2:
        tournament_year_placement = "20" + tournament_title_placement.split(" ")[1]

    #tournament_year_placement = str(tournament_title_placement).split(" ")[1].replace("VGC", "")

    placement_links = soup.find_all("h2")



    i = 1
    for placement in placement_links:


         trainer_placement_string = placement.text


         placement_names_sub = re.sub(r'\([^)]*\)', '', trainer_placement_string)

         trainer_names.append(placement_names_sub)

         trainer_nationalities_string = trainer_placement_string[trainer_placement_string.find("(")+1:trainer_placement_string.find(")")]

         trainer_nationalities.append(trainer_nationalities_string)



         placement_dictionary[placement_names_sub] = trainer_nationalities_string, i, tournament_title_placement, tournament_year_placement

         #print("key added")

         i = i + 1

# Gets Placement table info from those events that DO NOT include nationality
placement_no_nat_names = []
placement_nationalities2 = []



for url in urls_without_nationalities:
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    placement_links_no_nat = soup.find_all("h2")

    tournament_title2 = soup.select("h1")[0].text.strip()

    if len(tournament_title2.split(" ")[0]) == 7:
        tournament_year2 = tournament_title2.split(" ")[0].replace("VGC", "")

    if len(tournament_title2.split(" ")[1]) == 4:
        tournament_year2 = tournament_title2.split(" ")[1]

    if len(tournament_title2.split(" ")[1]) == 2:
        tournament_year2 = "20" + tournament_title2.split(" ")[1]

    #tournament_year2 = "20" + str(tournament_title2).split(" ")[1]

    j = 1
    for placement in placement_links_no_nat:

        placement_names_string_no_nat = unidecode.unidecode(placement.text)
        placement_names_sub_no_nat = re.sub(r'\([^)]*\)', '', placement_names_string_no_nat)

        placement_no_nat_names.append(unidecode.unidecode(placement_names_sub_no_nat))

        placement_nationalities_string2 = placement_names_string_no_nat[
                                       placement_names_string_no_nat.find("(") + 1:placement_names_string_no_nat.find(")")]

        placement_nationalities2.append(placement_nationalities_string2)

        #print(placement_no_nat_names[0], placement_nationalities2[0])
        #print(placement_names_string_no_nat, placement_nationalities_string2)

        if placement_nationalities_string2 in placement_names_string_no_nat:
                # and trainer_names_string[1] == trainer_nationalities_string[1] \
                # and trainer_names_string[2] == trainer_nationalities_string[2]:


            #placement_dictionary[placement_names_sub_no_nat] = "none"

            placement_dictionary[
                    placement_names_sub_no_nat] = "none", j, tournament_title2, tournament_year2
            j = j + 1





#%%%%%%%%%%%%% End of Trainer, Tournament, Competes, Team info

abilities_df.to_sql("ability", engine, if_exists="append", index=False)

moves_df.to_sql("move", engine, if_exists="append", index=False)

#insert the pokemon datafram into a table
species_df.to_sql("species", engine, if_exists="append")

#insert the has_ability_df
has_ability_df.to_sql("has_ability", engine, if_exists="append",index=False)

learns_move_df.to_sql("learns_move", engine, if_exists="append", index=False)

print(df_all_pokemon)
df_all_pokemon.to_sql("pokemon", engine, if_exists="append", index=False, chunksize=4)

df_hasMove.to_sql("has_move", engine, if_exists="append", index=False)

#write to tables for trainers, team, competes and tournaments goes here

# Loading the trainer dictionary into the Trainer table------------------------

sql = "INSERT INTO trainer (trainer_name, trainer_nationality) VALUES (%s, %s)"


for key in res:

        name_val = key
        nationality_val = res.get(key)

        all_vals = (name_val, nationality_val)


        mycursor.execute(sql, all_vals)

        mydb.commit()

# Inserting the tournament info into the Tournament table-----------------
sql = "INSERT INTO tournament (tournament_name, tournament_year) VALUES (%s, %s)"

for key in tournament_dictionary:

          title_val = key
          year_val = tournament_dictionary.get(key)

          all_vals = (title_val, year_val)


          mycursor.execute(sql, all_vals)
          mydb.commit()



# Loads placement info into the Placement table
sql = "INSERT INTO placement (trainer_name, trainer_nationality, placement, tournament_name, tournament_year) VALUES (%s, %s, %s, %s, %s)"
sql2 = "SET FOREIGN_KEY_CHECKS=0"
sql3 = "SET FOREIGN_KEY_CHECKS=1"
for key in placement_dictionary:

          name_val_p = key
          other_val_p = placement_dictionary.get(key)


          all_vals_p = (name_val_p, *other_val_p)


          mycursor.execute(sql2)
          mycursor.execute(sql, all_vals_p)
          mycursor.execute(sql3)
          mydb.commit()

