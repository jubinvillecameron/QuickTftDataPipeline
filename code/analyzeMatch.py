#Goal here is to analyze match by match build a dictionary, so each player's spot their placement augments etc
#then put it into my sql database which i can then use in tableau

import json
import requests
from keys import key

def analyze_match():
    """
    Game data is turned into boards.json, matches.json, and players.json
    """

    print("Analyzing match")

    with open("data/game_data.json") as f:
        data = json.load(f)




    boards = {}



    #so basic idea here is check the match then seperate it into match, player, board
    for game in data.keys():

        boards[game] = {}


        matchInfos = {}

        matchInfos['id'] = game
        matchInfos['date'] = data[game]['info']["game_datetime"]
        
        patch = data[game]['info']['game_version']
        patch.split()

        patch = patch.split()

        patch = patch[2]
        patch = patch[:5]

        matchInfos['patch'] = patch

        boards[game]['matchInfo'] = matchInfos

        metaParticipants = data[game]['metadata']['participants']


        gameParticipants = []
        #grab all participants and their respective names
        #print(metaParticipants)
        for participant in metaParticipants:
            playerInfo = {}
            
            try:
                userData = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{participant}?api_key={key}")
                #print(userData)
                userData = userData.json()
                #print(userData)

            except:
                #print(userData)
                pass

            username = userData['gameName']

            tag = userData['tagLine']

            username = username + "#" + tag


            playerInfo['username'] = username
            playerInfo['puuid'] = participant

            gameParticipants.append(playerInfo)
        
        print(gameParticipants)
        #append the correct players 
        boards[game]['players'] = gameParticipants

        participants = data[game]['info']['participants']

        curboard = []
        #grabbing just the boards now
        for participant in participants:

            board = {}
            board['puuid'] = participant['puuid']
            board['augments'] = participant['augments']
            board['placement'] = participant['placement']
            board['traits'] = participant['traits']
            board['units'] = participant['units']
            board['matchId'] = game

            curboard.append(board)
        
        boards[game]['boards'] = curboard


    # with open("data/matches.json", "w") as f:
    #     json.dump(matches, f, indent=4)

    # with open("data/players.json", "w") as f2:
    #     json.dump(players, f2, indent=4)
        
    with open("data/boards.json", "w") as f3:
        json.dump(boards, f3, indent=4)


if __name__ == "__main__":
    analyze_match()
