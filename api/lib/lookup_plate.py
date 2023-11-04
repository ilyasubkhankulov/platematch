import requests
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
PLATETOVIN_BASE_URL = "https://platetovin.com"

from dataclasses import dataclass


class VinInfo(BaseModel):
    vin: str
    year: str
    make: str
    model: str
    trim: str
    name: str
    engine: str
    style: str
    transmission: str
    driveType: str
    fuel: str
    color: dict


class VinResponse(BaseModel):
    success: bool
    vin: VinInfo


def lookup_plate(plate: str, state: str):
    url = PLATETOVIN_BASE_URL + "/api/convert"
    payload = {
        "state": state,
        "plate": plate,
    }
    headers = {
        "Authorization": os.getenv("PLATETOVIN_API_KEY"),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    if response.status_code == 200:
        return VinResponse(**json.loads(response.content.decode("utf-8")))
    else:
        return None


if __name__ == "__main__":
    print(lookup_plate("8uea243", "CA"))
