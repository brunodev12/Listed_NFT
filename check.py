import requests
import json
import os
from mail import send_email
from unclaimedNFTs import un_claimed_NFTs

api_key=os.environ.get('API_KEY')
collection=os.environ.get('COLLECTION')

unClaimed = None
listed = None
unClaimed_listed = []

def doubleCheck(_tokenId):

    url = f"{api_key}/byItem?type=LIST&type=SELL&type=TRANSFER&itemId=POLYGON%3A{collection}%3A{_tokenId}&size=3&sort=LATEST_FIRST"

    _headers = {
    "accept": "application/json"
    }

    r = requests.get(url, headers=_headers)

    data = r.json()
    if len(data['activities'])>0:
        if data['activities'][0]['@type'] == 'LIST':
            coin = data['activities'][0]['take']['type']['@type']
            coin_name = 'WETH' if coin=='ERC20' else 'MATIC'
            value = float(data['activities'][0]['take']['value'])
            if (coin_name=='MATIC' and value<26) or (coin_name=='WETH' and value <0.015):
                return True
    return False

with open("unClaimedNft.json") as jsonfile_1:
    unClaimed = json.load(jsonfile_1)

with open("listedNft.json") as jsonfile_2:
    listed = json.load(jsonfile_2)

unClaimed_list = []

for i in unClaimed:
    token = int(i['tokenId'])
    unClaimed_list.append(token)

tokens = []

for i in listed:
    if (i['tokenId'] in unClaimed_list):
        print(i)
        if (doubleCheck(i['tokenId'])) and (i['tokenId'] not in tokens):
            unClaimed_listed.append(i)
            tokens.append(i['tokenId'])
            
with open("unClaimed_listed.json", "w") as jsonfile:
    json.dump(unClaimed_listed, jsonfile)


if len(unClaimed_listed)>0:
    send_email(unClaimed_listed, 'Unclaimed NFTs found')
    un_claimed_NFTs()

