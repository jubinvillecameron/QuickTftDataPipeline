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

    metaParticipants = data[game]['metadata']['participants']

    playerInfo = {}

    #grab all participants and their respective names
    for participant in metaParticipants:
        
        try:
            userData = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{participant}?api_key={key}")
            #print(userData)
            userData = userData.json()

        except:
            #print(userData)
            pass

        username = userData['gameName']


        tag = userData['tagLine']

        username = username + "#" + tag


        playerInfo['username'] = username
        playerInfo['puuid'] = participant

        players.append(playerInfo)

    participants = data[game]['info']['participants']

    for participant in participants:

        board = {}

        board['puuid'] = participant['puuid']
        board['augments'] = participant['augments']
        board['placement'] = participant['placement']
        board['traits'] = participant['traits']
        board['units'] = participant['units']
        board['matchId'] = game

        boards.append(board)



with open("data/matches.json", "w") as f:
    json.dump(matches, f, indent=4)

with open("data/players.json", "w") as f2:
    json.dump(players, f2, indent=4)
    
with open("data/boards.json", "w") as f3:
    json.dump(boards, f3, indent=4)
