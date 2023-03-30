import requests
import json
import os

api_key=os.environ.get('API_KEY')
collection=os.environ.get('COLLECTION')

url = f"{api_key}/byCollection?type=LIST&collection=POLYGON%3A{collection}&size=50&sort=LATEST_FIRST"

_headers = {
    "accept": "application/json"
}

r = requests.get(url, headers=_headers)

data = r.json()

elements = []

def saveElements(_tokenId, _price, _symbol, _source):
    _tokenId = int(_tokenId)
    _price = float(_price)
    elements.append({'tokenId': _tokenId, 'price': _price, 'symbol': _symbol, 'exchange': _source})

for i in data['activities']:
    tokenId = i['make']['type']['tokenId']
    price = i['price']
    if i['take']['type']['@type']=='ERC20':
        try:
            if i['take']['type']['contract']=='POLYGON:0x7ceb23fd6bc0add59e62ac25578270cff1b9f619':
                symbol = 'WETH'
            else:
                symbol = 'OTHER'
        except:
            symbol = 'OTHER'
    else:
        symbol = 'MATIC'
    source = i['source']
    print('tokenId:', tokenId, 'price:', price, symbol, 'exchange:', source)
    saveElements(tokenId, price, symbol, source)

with open("listedNft.json", "w") as jsonfile:
    json.dump(elements, jsonfile)


