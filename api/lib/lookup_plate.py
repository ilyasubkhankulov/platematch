import json
import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
XRAPID_API_KEY = os.getenv("XRAPID_API_KEY")

class VinInfo(BaseModel):
    vin: str
    year: str
    make: str
    model: str
    trim: str
    engine: str
    style: str
    made_in: str
    steering_type: str
    anti_brake_system: str
    type: str
    overall_height: str
    overall_length: str
    overall_width: str
    standard_seating: str
    highway_mileage: str
    city_mileage: str
    fuel_type: str
    drive_type: str
    transmission: str

class VinResponse(BaseModel):
    specifications: VinInfo
    vin: str


def get_vin(plate: str, state: str):
    url = "https://us-license-plate-to-vin.p.rapidapi.com/licenseplate"
    querystring = {"plate": plate, "state": state}

    headers = {
        "X-RapidAPI-Key": XRAPID_API_KEY,
        "X-RapidAPI-Host": "us-license-plate-to-vin.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print("get_vin", response.json())
    return response.json()

# get_vin {'plate': '6mxk969', 'state': 'CA', 'specifications': {'vin': 'JTHBK262165014930'}}

def get_plate_info(vin: str):
    url = "https://vin-decoder7.p.rapidapi.com/vin"

    querystring = {"vin": vin}

    headers = {
        "X-RapidAPI-Key": XRAPID_API_KEY,
        "X-RapidAPI-Host": "vin-decoder7.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("get_plate_info", response.json())
    response_object = VinResponse(**json.loads(
        response.content.decode("utf-8")))
    return response_object


def lookup_plate(plate: str, state: str):
    vin_response = get_vin(plate, state)
    vin = vin_response["specifications"]["vin"]
    print('vin: ', vin)
    plate_info = get_plate_info(vin)
    return plate_info

# get_plate_info {'vin': 'JTHBK262165014930', 'specifications': {'vin': 'JTHBK262165014930', 'year': '2006', 'make': 'Lexus', 'model': 'IS', 'trim': 'IS 250', 'engine': '2.5-L V-6 24V DOHC', 'style': '6-Speed Manual', 'made_in': 'Japan', 'steering_type': 'Rack & Pinion', 'anti_brake_system': '4-Wheel ABS', 'type': 'Sedan', 'overall_height': '56.10 inches', 'overall_length': '180.10 inches', 'overall_width': '70.90 inches', 'standard_seating': '5', 'highway_mileage': '29 miles/gallon', 'city_mileage': '20 miles/gallon', 'fuel_type': 'Premium (Required)', 'drive_type': 'Rear-Wheel Drive', 'transmission': '6-Speed Manual'}}

if __name__ == "__main__":
    print(lookup_plate("8UEA243", "CA"))

# example_plate = VinResponse(
#     success=True,
#     vin=VinInfo(
#         vin="3TMMU4FN7FM086431",
#         year="2015",
#         make="Toyota",
#         model="Tacoma",
#         trim="Delux Grade",
#         name="2015 Toyota Tacoma",
#         engine="4.0L V6 DOHC",
#         style="PICKUP",
#         transmission="",
#         driveType="4WD/4-Wheel Drive/4x4",
#         fuel="Gasoline",
#         color=Color(name="Unknown", abbreviation="UNK"),
#     ),
# )