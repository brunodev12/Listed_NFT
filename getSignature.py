import requests
import os

api_key = os.environ.get('API_KEY3')

def get_signature(id):
    url = f"{api_key}/order/signature/seaport/simple/{id}"

    _headers = {
        "accept": "application/json"
    }

    r = requests.get(url, headers=_headers)
    r_json = r.json()
    signature = r_json['signature']
    return signature
