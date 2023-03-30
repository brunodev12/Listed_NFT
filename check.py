import requests
import json
import os
from mail import send_email

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
        return data['activities'][0]['@type'] == 'LIST'
    
    return False

with open("unClaimedNft.json") as jsonfile_1:
    unClaimed = json.load(jsonfile_1)

with open("listedNft.json") as jsonfile_2:
    listed = json.load(jsonfile_2)

unClaimed_list = []

for i in unClaimed:
    token = int(i['tokenId'])
    unClaimed_list.append(token)

for i in listed:
    if (i['tokenId'] in unClaimed_list):
        print(i)
        if doubleCheck(i['tokenId']):
            if (i['symbol']=='WETH' and i['price']<0.023) or (i['symbol']=='MATIC' and i['price']<37) or (i['symbol']=='OTHER'):
                unClaimed_listed.append(i)
            

if len(unClaimed_listed)>0:
    send_email(unClaimed_listed)

