from enum import Enum
from dotenv import load_dotenv
import os

from dataclasses import dataclass
from typing import List, Optional, Union


class ResponseStatus(Enum):
    FORBIDDEN = 403  # CRITICAL PAY FOR THE API
    PAYLOAD_TOO_LARGE = 413  # CRITICAL FIX THE PREPROCESSING
    TOO_MANY_REQUESTS = 429  # TRY AGAIN AFTER ONE SECOND
    OK = 200  # OK


load_dotenv()
PLATE_RECOGNIZER_API = os.getenv("PLATE_RECOGNIZER_API")


@dataclass
class Box:
    xmin: int
    ymin: int
    xmax: int
    ymax: int


@dataclass
class Region:
    code: str
    score: float


@dataclass
class Vehicle:
    score: float
    type: str
    box: Box


@dataclass
class Candidate:
    score: float
    plate: str


@dataclass
class ModelMake:
    make: str
    model: str
    score: float


@dataclass
class Color:
    color: str
    score: float


@dataclass
class Orientation:
    orientation: str
    score: float


@dataclass
class Result:
    box: Box
    plate: str
    region: Region
    vehicle: Vehicle
    score: float
    candidates: List[Candidate]
    dscore: float
    model_make: List[ModelMake]
    color: List[Color]
    orientation: List[Orientation]


@dataclass
class LicensePlateData:
    processing_time: float
    results: List[Result]
    filename: str
    version: int
    camera_id: Optional[str]
    timestamp: str


@dataclass
class Response:
    status: ResponseStatus
    data: Union[LicensePlateData, None]


from io import BufferedReader
import requests


def get_license_plate(image: BufferedReader) -> Response:
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
        return Response(status=ResponseStatus.FORBIDDEN, data=None)
    elif response.status_code == 413:
        print(
            "Payload Too Large response status code indicates that the request entity is larger than limits defined by our server. See upload limits."
        )
        return Response(status=ResponseStatus.PAYLOAD_TOO_LARGE, data=None)
    elif response.status_code == 429:
        print(
            "Indicates the user has sent too many requests in a given amount of time. The Free Trial Snapshot API Cloud Plan has a limit of 1 lookup per second. A Snapshot API Cloud Subscription has a limit of 8 lookups per second. The Snapshot SDK does not have any lookup limits per second. Subscribe for a higher number of calls per second for your API Cloud plan. The response is {'detail':'Request was throttled. Expected available in 1 second.','status_code':429}."
        )
        return Response(status=ResponseStatus.TOO_MANY_REQUESTS, data=None)
    else:
        data = response.json()
        return Response(status=ResponseStatus.OK, data=LicensePlateData(**data))
