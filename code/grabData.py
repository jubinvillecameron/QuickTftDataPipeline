from keys import key

import requests
import json

gameName = "CamWavy"
tagLine = "NA1"

americas = "https://americas.api.riotgames.com"

#Grabs account puuid for further fetches
accountReq = requests.get(f"{americas}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={key}")
accountInfo = accountReq.json()
puuid = accountInfo["puuid"]

print("Puuid grabbed")

na1 = "https://na1.api.riotgames.com"


#Now grab recent 20 matches, can even grab like 100 games in future

twentyGames = requests.get(f"{americas}/tft/match/v1/matches/by-puuid/{puuid}/ids?api_key={key}")
print(twentyGames.json())

matchInfo = {}

for game in twentyGames.json():

    match = requests.get(f"{americas}/tft/match/v1/matches/{game}?api_key={key}")
    game_id = match.json()["metadata"]["match_id"]
    matchInfo[game_id] = match.json()

with open("data/game_data.json", "w") as f:
    json.dump(matchInfo, f, indent=4)




