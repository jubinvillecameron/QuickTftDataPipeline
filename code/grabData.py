from keys import key

import requests
import json

def get_gamedata(puuid):
    """
    Created gamedata.json off of given puuid
    """

    # gameName = "CamWavy"
    # tagLine = "NA1"

    americas = "https://americas.api.riotgames.com"

    # #Grabs account puuid for further fetches
    # accountReq = requests.get(f"{americas}/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={key}")
    # accountInfo = accountReq.json()
    # puuid = accountInfo["puuid"]

    # print("Puuid grabbed", puuid)

    na1 = "https://na1.api.riotgames.com"


    #Now grab recent 10 matches so we're not rate limited

    print("grabbing 10 games")
    tenGames = requests.get(f"{americas}/tft/match/v1/matches/by-puuid/{puuid}/ids?count=10&api_key={key}")
    #print(tenGames.json())

    matchInfo = {}

    for game in tenGames.json():

        match = requests.get(f"{americas}/tft/match/v1/matches/{game}?api_key={key}")

        #1100 = tft ranked
        if (match.json()["info"]['queueId'] == 1100):
            matchInfo[game] = match.json()

    with open("data/game_data.json", "w") as f:
        json.dump(matchInfo, f, indent=4)



def grab_challengers(rank):
    """
    Returns the puuid from the specified rank of challenger
    """

    if not (1 <= rank <= 200):
        raise(Exception)


    #Doing gm players right now since it's the start of the season
    #challengers = requests.get(f"https://na1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT&api_key={key}")
    challengers = requests.get(f"https://na1.api.riotgames.com/tft/league/v1/grandmaster?queue=RANKED_TFT&api_key={key}")

    challengers = challengers.json()


    #entries is where I get the specific challengers puuid
    challengerEntries = challengers["entries"]

    for index, value in enumerate(challengerEntries):
        
        if(index + 1 == rank):
            return grab_puuid_summonerid(value)
        
def grab_puuid_summonerid(value):

    summonerid = value["summonerId"]

    puuid = requests.get(f"https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{summonerid}?api_key={key}")

    return puuid.json()[0]["puuid"]





if __name__ == "__main__":
   get_gamedata(grab_challengers(1))




