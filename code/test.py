
import json
from keys import key
import requests

userData = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/P4BDoSxED81AxmzZ9C2M_j8GlgJFFvOdcC0MuXfALxT1fAVX9R0FnT36CGjimmfJuTeBIpkLFP0V9A?api_key={key}")
userData = userData.json()

print(userData['gameName'])

    
