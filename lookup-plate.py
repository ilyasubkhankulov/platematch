import requests
import json

PLATETOVIN_API_KEY='JIms37w6L2ngsSv'
PLATETOVIN_BASE_URL='https://platetovin.com/'


def lookup_plate(plate: str, state: str):
    url = PLATETOVIN_BASE_URL + '/api/convert'
    payload = {
        "state": state,
        "plate": plate,
    }
    headers = {
    'Authorization': 'YOUR API KEY',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }

    response = requests.request('POST', url, headers=headers, json=payload)
    response.json()
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None