import os
import uuid

from dotenv import load_dotenv
from lib.match_car import CarMatch, ComparisonResult, ComparisonValue, MatchResult
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


class ImageMetadata(BaseModel):
    lat: str
    long: str


def get_records() -> list[(str, str, CarMatch)]:
    response = supabase.table("VehicleComparison").select("*").execute()
    print(response)
    responseMatches: list[(str, str, float, float, CarMatch)] = []
    for resp in response.data:
        print(resp)
        carMatchResult: CarMatch = CarMatch(
            overall_result=MatchResult.from_string(
                resp["overall_match_result"]),
            make_result=ComparisonResult(
                match_result=MatchResult.from_string(
                    resp["make_match_result"]),
                field_name=ComparisonValue.MAKE,
                plate_value=resp["make_plate_value"],
                car_value=resp["make_car_value"],
            ),
            model_result=ComparisonResult(
                match_result=MatchResult.from_string(
                    resp["model_match_result"]),
                field_name=ComparisonValue.MODEL,
                plate_value=resp["model_plate_value"],
                car_value=resp["model_car_value"],
            ),
            year_result=ComparisonResult(
                match_result=MatchResult.from_string(
                    resp["year_match_result"]),
                field_name=ComparisonValue.YEAR,
                plate_value=resp["year_plate_value"],
                car_value=resp["year_car_value"],
            ),
        )
        responseMatches.append(
            (resp["id"], resp["object_name"], resp['latitude'],
             resp['longitude'], carMatchResult))
    records = [obj_to_dict(record) for record in responseMatches]
    return records


def get_record(id: int) -> (str, str, CarMatch):
    response = supabase.table("VehicleComparison").select(
        "*").eq("id", id).execute()
    if len(response.data) == 0:
        return None, None, "No record found"
    resp = response.data[0]
    carMatchResult: CarMatch = CarMatch(
        overall_result=MatchResult.from_string(resp["overall_match_result"]),
        make_result=ComparisonResult(
            match_result=MatchResult.from_string(resp["make_match_result"]),
            field_name=ComparisonValue.MAKE,
            plate_value=resp["make_plate_value"],
            car_value=resp["make_car_value"],
        ),
        model_result=ComparisonResult(
            match_result=MatchResult.from_string(resp["model_match_result"]),
            field_name=ComparisonValue.MODEL,
            plate_value=resp["model_plate_value"],
            car_value=resp["model_car_value"],
        ),
        year_result=ComparisonResult(
            match_result=MatchResult.from_string(resp["year_match_result"]),
            field_name=ComparisonValue.YEAR,
            plate_value=resp["year_plate_value"],
            car_value=resp["year_car_value"],
        ),
    )
    return resp["id"], resp["object_name"], carMatchResult


def save_record(record: CarMatch, object_name: str, location: ImageMetadata):
    data, count = (
        supabase.table("VehicleComparison")
        .insert(
            {
                "overall_match_result": record.overall_result.name,
                "make_match_result": record.make_result.match_result.name,
                "make_plate_value": record.make_result.plate_value,
                "make_car_value": record.make_result.car_value,
                "model_match_result": record.model_result.match_result.name,
                "model_plate_value": record.model_result.plate_value,
                "model_car_value": record.model_result.car_value,
                "year_match_result": record.year_result.match_result.name,
                "year_plate_value": record.year_result.plate_value,
                "year_car_value": record.year_result.car_value,
                "latitude": location.lat if location else None,
                "longitude": location.long if location else None,
                "object_name": object_name if object_name else None,
            }
        )
        .execute()
    )
    return data, count


def save_image(image_path) -> str:
    # generate file name
    name = str(uuid.uuid4())
    with open(image_path, "rb") as image:
        supabase.storage.from_("car-photos").upload(
            file=image, path=f"{name}.png", file_options={"content-type": "image/png"}
        )
    return name


def load_image(name: str) -> str:
    # generate file name
    res = supabase.storage.from_("car-photos").download(path=f"{name}.png")
    print(type(res))
    return res


def obj_to_dict(obj):
    if isinstance(obj, tuple):
        print(obj)
        # Get the first element in tuple as id
        id, _,  latitude, longitude, car_match = obj
        # id _, object_name, latitude, longitude, car_match = obj
        return {"id": id, "latitude": latitude, "longitude": longitude,
                "car_match": obj_to_dict(car_match)}
    elif isinstance(obj, CarMatch):
        return {
            "overall_result": obj.overall_result.name,
            "make_result": obj_to_dict(obj.make_result),
            "model_result": obj_to_dict(obj.model_result),
            "year_result": obj_to_dict(obj.year_result),
        }
    elif isinstance(obj, ComparisonResult):
        return {
            "match_result": obj.match_result.name,
            "field_name": obj.field_name.name,
            "plate_value": obj.plate_value,
            "car_value": obj.car_value,
        }
    elif isinstance(obj, (MatchResult, ComparisonValue)):
        return obj.name
    else:
        return obj
