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

print("Puuid grabbed", puuid)

na1 = "https://na1.api.riotgames.com"


#Now grab recent 10 matches so we're not rate limited

print("grabbing 10 games")
tenGames = requests.get(f"{americas}/tft/match/v1/matches/by-puuid/{puuid}/ids?count=10&api_key={key}")
print(tenGames.json())

matchInfo = {}

for game in tenGames.json():

    match = requests.get(f"{americas}/tft/match/v1/matches/{game}?api_key={key}")

    if (match.json()["info"]['queueId'] == 1100):
        matchInfo[game] = match.json()

with open("data/game_data.json", "w") as f:
    json.dump(matchInfo, f, indent=4)




