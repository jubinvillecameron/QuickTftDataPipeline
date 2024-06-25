#Goal here is to analyze match by match build a dictionary, so each player's spot their placement augments etc
#then put it into my sql database which i can then use in tableau

import json
import requests
from keys import key

with open("data/game_data.json") as f:
    data = json.load(f)




matches = []
players = []
boards = []



#so basic idea here is check the match then seperate it into match, player, board
for game in data.keys():


    matchInfos = {}

    matchInfos['id'] = game
    matchInfos['date'] = data[game]['info']["game_datetime"]
    
    patch = data[game]['info']['game_version']
    patch.split()

    patch = patch.split()

    patch = patch[2]
    patch = patch[:5]

    matchInfos['patch'] = patch

    matches.append(matchInfos)

    playerInfo = {}

    participants = data[game]['info']['participants']

    puuid = participants['puuid']

    #now grab the users actual username
    userData = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={key}")
    username = userData['gameName']
    tag = userData['tagLine']
    username = username + "#" + tag
    playerInfo['username'] = username
    playerInfo['puuid'] = puuid

    players.append(playerInfo)

    #seperate board state -> traits, level, augments, units

    pass


