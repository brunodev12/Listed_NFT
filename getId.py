import requests
from decouple import config

api_key = config('API_KEY2')
collection = config('COLLECTION')

def get_id(token_id):

    url = f"{api_key}/orders/sell/byItem?platform=OPEN_SEA&itemId=POLYGON%3A{collection}%3A{token_id}&status=ACTIVE"

    _headers = {
        "accept": "application/json"
    }

    r = requests.get(url, headers=_headers)
    data = r.json()
    return data