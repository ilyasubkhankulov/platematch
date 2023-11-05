from enum import Enum
from dotenv import load_dotenv
import os

from typing import List, Optional, Union

from pydantic import BaseModel

from io import BytesIO
import requests


class ResponseStatus(Enum):
    FORBIDDEN = 403  # CRITICAL PAY FOR THE API
    PAYLOAD_TOO_LARGE = 413  # CRITICAL FIX THE PREPROCESSING
    TOO_MANY_REQUESTS = 429  # TRY AGAIN AFTER ONE SECOND
    OK = 200  # OK


load_dotenv()
PLATE_RECOGNIZER_API = os.getenv("PLATE_RECOGNIZER_API")


class Box(BaseModel):
    xmin: int
    ymin: int
    xmax: int
    ymax: int


class Region(BaseModel):
    code: str
    score: float


class Vehicle(BaseModel):
    score: float
    type: str
    box: Box


class Candidate(BaseModel):
    score: float
    plate: str


class ModelMake(BaseModel):
    make: str
    model: str
    score: float


class Color(BaseModel):
    color: str
    score: float


class Orientation(BaseModel):
    orientation: str
    score: float


class Result(BaseModel):
    box: Box
    plate: str
    region: Region
    vehicle: Vehicle
    score: float
    candidates: List[Candidate]
    dscore: float
    # model_make: Union[List[ModelMake], None]
    # color: Union[List[Color], None]
    # orientation: Union[List[Orientation], None]


class LicensePlateData(BaseModel):
    processing_time: float
    results: List[Result]
    filename: str
    version: int
    camera_id: Optional[str]
    timestamp: str


class LicensePlateResponse(BaseModel):
    status: ResponseStatus
    data: Union[LicensePlateData, None]


def get_license_plate(image: BytesIO) -> LicensePlateResponse:
    regions = ["mx", "us-ca"]  # Change to your country
    response = requests.post(
        "https://api.platerecognizer.com/v1/plate-reader/",
        data=dict(regions=regions),  # Optional
        files=dict(upload=image),
        headers={"Authorization": f"Token {PLATE_RECOGNIZER_API}"},
    )

    if response.status_code == 403:
        print(
            "Forbidden: you do not have enough credits to perform this request or your API key is wrong."
        )
        return LicensePlateResponse(status=ResponseStatus.FORBIDDEN, data=None)
    elif response.status_code == 413:
        print(
            "Payload Too Large response status code indicates that the request entity is larger than limits defined by our server. See upload limits."
        )
        return LicensePlateResponse(status=ResponseStatus.PAYLOAD_TOO_LARGE, data=None)
    elif response.status_code == 429:
        print(
            "Indicates the user has sent too many requests in a given amount of time. The Free Trial Snapshot API Cloud Plan has a limit of 1 lookup per second. A Snapshot API Cloud Subscription has a limit of 8 lookups per second. The Snapshot SDK does not have any lookup limits per second. Subscribe for a higher number of calls per second for your API Cloud plan. The response is {'detail':'Request was throttled. Expected available in 1 second.','status_code':429}."
        )
        return LicensePlateResponse(status=ResponseStatus.TOO_MANY_REQUESTS, data=None)
    else:
        data = response.json()
        print(f"DATA: {data}")
        return LicensePlateResponse(
            status=ResponseStatus.OK, data=LicensePlateData(**data)
        )
