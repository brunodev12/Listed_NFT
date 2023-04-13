import requests
import json
import os
from mail import send_email

url = os.environ.get('PRIVATE_URL')

def un_claimed_NFTs():
    try:
        data = requests.get(url)
        lista = data.json()['unclaimedNFTs']

        with open("unClaimedNft.json", "w") as jsonfile:
            json.dump(lista, jsonfile)
        
        return True
    except:
        send_email("There are no updates on unclaimed NFTs", 'No updates NFT')
        return False
