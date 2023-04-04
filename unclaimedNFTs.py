import requests
import json
import os

url = os.environ.get('PRIVATE_URL')

def un_claimed_NFTs():
    try:
        data = requests.get(url)
        lista = data.json()['unclaimedNFTs']


        with open("unClaimedNft.json", "w") as jsonfile:
            json.dump(lista, jsonfile)
    except KeyError:
        print("There are no updates on unclaimed NFTs")
