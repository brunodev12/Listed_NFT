import requests
import json
import os

url = os.environ.get('PRIVATE_URL')

data = requests.get(url)
lista = data.json()['unclaimedNFTs']


with open("unClaimedNft.json", "w") as jsonfile:
    json.dump(lista, jsonfile)
