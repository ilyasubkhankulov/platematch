
<<<<<<< HEAD
import base64
=======
>>>>>>> c55363e (remove)
import json
import os
from io import BufferedReader
from typing import Annotated, Optional, Union

import aiofiles

# from lib.convert_image import heic_to_png_buffer
from constants import TMP_DIR
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from lib.database import (
    ImageMetadata,
    get_record,
    get_records,
    load_image,
    save_image,
    save_record,
)
from lib.image_preprocessing import make_png_buffer, open_heic_image, resize_image
from lib.license_plate_recognition import get_license_plate
from lib.lookup_plate import VinResponse, lookup_plate
from lib.match_car import CarMatch, match_car
from lib.recognize_car import recognize_car
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.get("/")(lambda: {"Hello": "World"})


async def save_to_disk(image, tmp_dir):
    # save the file
    path = os.path.join(tmp_dir, image.filename)
    async with aiofiles.open(path, "wb") as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write
    return path


class Error(BaseModel):
    error: str


@app.post("/upload/")
async def upload_image(
    lat: Annotated[float, Form()],
    long: Annotated[float, Form()],
    image: UploadFile = File(...),
) -> Union[CarMatch, Error]:
    # print(lat)
    # print(long)
    path = await save_to_disk(image, TMP_DIR)
    print("image saved to disk: ", path)

    # Getting license plate from the image
    heic_image = open_heic_image(path)
    heic_resized = resize_image(heic_image)
    png_buffer = make_png_buffer(heic_resized)
    license_plates_info = get_license_plate(png_buffer)

    if license_plates_info.data is None:
        return Error(error="Not found any")

    vin_responses: list[VinResponse] = []
    for result in license_plates_info.data.results:
        print(result)
        plate = result.plate
        code = result.region.code
        if code.split("-")[0] == "us":
            code = code.split("-")[1].upper()
        else:
            return Error(error="Not USA country plate")
        print("looking up plate")
        vin_response = lookup_plate(plate, code)

        if vin_response is None:
            return Error(error="Plate is invalid")

        vin_responses.append(vin_response)

    car_recognition = recognize_car(png_buffer)

    if car_recognition is None:
        return Error(error="Car is not recognized")

    for vin_response in vin_responses:
        car_match = match_car(vin_response, car_recognition)
        name = save_image(path)
        save_record(
            car_match, name, ImageMetadata(lat=str(lat), long=str(long))
        )  # ImageMetadata(lat=lat, long=long))
        return car_match

    return Error(error="No car have matched")


@app.post("/incident-report/")
async def incident_report(id: str = Form(...)):
    _, uuid, match_report = get_record(int(id))
    image_bytes = load_image(uuid)
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    response_data = {
        "image": image_base64,
        "info": match_report,
    }
    return response_data


@app.get("/incidents")
async def get_incidents():
    records = get_records()

    print(records)
    return JSONResponse(content=records)


# @app.post("/license-plate-ocr/")
# async def extract_license(image: UploadFile = File(...)):
#     path = await save_to_disk(image, TMP_DIR)
#     print("image saved to disk: ", path)

#     ## Getting license plate from the image
#     heic_image = open_heic_image(path)
#     heic_resized = resize_image(heic_image)
#     png_buffer = make_png_buffer(heic_resized)
#     print(license_plates_info)
#     json_data = jsonable_encoder(license_plates_info.data.results[0].plate)

#     return JSONResponse(content=json_data)


# @app.post("/recognize-car/")
# async def recognize_car_api(image: UploadFile = File(...)):
#     path = await save_to_disk(image, TMP_DIR)
#     print("image saved to disk: ", path)

#     ## Getting license plate from the image
#     heic_image = open_heic_image(path)
#     heic_resized = resize_image(heic_image)
#     png_buffer = make_png_buffer(heic_resized)
#     car_recognition = recognize_car(png_buffer)
#     print(car_recognition)
#     json_data = jsonable_encoder(car_recognition)

#     return JSONResponse(content=json_data)


# @app.post("/lookup-plate/")
# async def lookup_plate(plate: str = Form(...), state_code: str = Form(...)):
#     print(plate, state_code)
#     vin_response = lookup_plate(plate, state_code)
#     print(vin_response)
#     json_data = jsonable_encoder(vin_response)

#     return JSONResponse(content=json_data)
