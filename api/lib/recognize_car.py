from io import BufferedReader, BytesIO
from typing import Union
import requests

from pydantic import BaseModel


class Car(BaseModel):
    make: str
    model: str
    generation: str
    years: str
    prob: str


class Color(BaseModel):
    name: str
    probability: float


class Angle(BaseModel):
    name: str
    probability: float


class Bbox(BaseModel):
    br_x: float
    br_y: float
    tl_x: float
    tl_y: float


class CarRecognition(BaseModel):
    car: Car
    color: Color
    angle: Angle
    bbox: Bbox


headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "https://carnet.ai",
    "Pragma": "no-cache",
    "Referer": "https://carnet.ai/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
}

# files = {
#     'imageFile': ('lexus.png', open('your_file_path.png', 'rb')),
# }

# response = requests.post('https://carnet.ai/recognize-file', headers=headers, files=files)


def recognize_car(image_bytes: BytesIO) -> Union[CarRecognition, None]:
    image_bytes.seek(0)
    files = {"imageFile": ("image.png", image_bytes)}
    response = requests.post(
        "https://carnet.ai/recognize-file", headers=headers, files=files
    )

    if response.status_code != 200:
        return None

    return CarRecognition(**response.json())
