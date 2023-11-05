import requests
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
PLATETOVIN_BASE_URL = "https://platetovin.com"

from dataclasses import dataclass


class Color(BaseModel):
    name: str
    abbreviation: str


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
    color: Color


class VinResponse(BaseModel):
    success: bool
    vin: VinInfo


def lookup_plate(plate: str, state: str):
    # url = PLATETOVIN_BASE_URL + "/api/convert"
    # payload = {
    #     "state": state,
    #     "plate": plate,
    # }
    # headers = {
    #     "Authorization": os.getenv("PLATETOVIN_API_KEY"),
    #     "Content-Type": "application/json",
    #     "Accept": "application/json",
    # }

    # response = requests.request("POST", url, headers=headers, json=payload)
    # print(response)
    # if response.status_code == 200:
    #     return VinResponse(**json.loads(response.content.decode("utf-8")))
    # else:
    #     return None
    return example_plate


if __name__ == "__main__":
    print(lookup_plate("8uea243", "CA"))

example_plate = VinResponse(
    success=True,
    vin=VinInfo(
        vin="3TMMU4FN7FM086431",
        year="2015",
        make="Toyota",
        model="Tacoma",
        trim="Delux Grade",
        name="2015 Toyota Tacoma",
        engine="4.0L V6 DOHC",
        style="PICKUP",
        transmission="",
        driveType="4WD/4-Wheel Drive/4x4",
        fuel="Gasoline",
        color=Color(name="Unknown", abbreviation="UNK"),
    ),
)