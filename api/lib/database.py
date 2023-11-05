import os
from supabase import create_client, Client
from dotenv import load_dotenv
from lib.match_car import CarMatch
from pydantic import BaseModel


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class ImageMetadata(BaseModel):
    lat: str
    long: str

def get_records():
    response = supabase.table('VehicleComparison').select("*").execute()
    return response

def save_record(record: CarMatch, location: ImageMetadata = None):
    print
    data, count = supabase.table('VehicleComparison').insert({
        'overall_match_result': record.overall_result.name,
        'make_match_result': record.make_result.match_result.name,
        'make_plate_value': record.make_result.plate_value,
        'make_car_value': record.make_result.car_value,
        'model_match_result': record.model_result.match_result.name,
        'model_plate_value': record.model_result.plate_value,
        'model_car_value': record.model_result.car_value,
        'year_match_result': record.year_result.match_result.name,
        'year_plate_value': record.year_result.plate_value,
        'year_car_value': record.year_result.car_value,
        'latitude': location.lat if location else None,
        'longitude': location.long if location else None,
        }).execute()
    return data, count
