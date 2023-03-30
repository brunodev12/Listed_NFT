import requests
import json
from decouple import config

url = config('PRIVATE_URL')

data = requests.get(url)
lista = data.json()['unclaimedNFTs']


with open("unClaimedNft.json", "w") as jsonfile:
    json.dump(lista, jsonfile)