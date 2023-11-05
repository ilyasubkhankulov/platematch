import os
from supabase import create_client, Client
from dotenv import load_dotenv
from lib.match_car import CarMatch, ComparisonResult
from pydantic import BaseModel


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class ImageMetadata(BaseModel):
    lat: str
    long: str

def get_records() -> list[CarMatch]:
    response = supabase.table('VehicleComparison').select("*").execute()
    responseMatches: list[CarMatch] = []
    for resp in response.data:
        carMatchResult: CarMatch = CarMatch(
            overall_result=resp['overall_match_result'],
            make_result=ComparisonResult(
                match_result=response['make_match_result'],
                make_plate_value=response['make_plate_value'],
                make_car_value=response['make_car_value']
            ),
            model_result=ComparisonResult(
                match_result=response['model_match_result'],
                model_plate_value=response['model_plate_value'],
                model_car_value=response['model_car_value']
            ),
            year_result=ComparisonResult(
                match_result=response['year_match_result'],
                year_plate_value=response['year_plate_value'],
                year_car_value=response['year_car_value']
            ),
        )
        responseMatches.append(carMatchResult)
    return responseMatches

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
