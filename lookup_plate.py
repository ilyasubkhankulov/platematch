import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
PLATETOVIN_BASE_URL='https://platetovin.com'


def lookup_plate(plate: str, state: str):
    url = PLATETOVIN_BASE_URL + '/api/convert'
    payload = {
        "state": state,
        "plate": plate,
    }
    headers = {
    'Authorization': os.getenv('PLATETOVIN_API_KEY'),
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, json=payload)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
if __name__ == '__main__':
    print(lookup_plate('36823S2', 'CA'))