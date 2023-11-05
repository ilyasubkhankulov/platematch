import json
import os
from typing import Optional, Union

import aiofiles

# from lib.convert_image import heic_to_png_buffer
from constants import TMP_DIR
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from lib.image_preprocessing import make_png_buffer, open_heic_image, resize_image
from lib.license_plate_recognition import get_license_plate
from lib.lookup_plate import VinResponse, lookup_plate
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


# class ImageMetadata(BaseModel):
#     lat: str
#     long: str


@app.post("/upload/")
async def upload_image(
        image: UploadFile = File(...),
        metadata: Union[str, None] = File(None)):
   
    if (metadata is not None):
        metadata_dict = json.loads(metadata)
        print("inputted metadata: ", metadata_dict)
    else:
        metadata_dict = None

    path = await save_to_disk(image, TMP_DIR)
    print("image saved to disk: ", path)

    ## Getting license plate from the image
    heic_image = open_heic_image(path)
    heic_resized = resize_image(heic_image)
    png_buffer = make_png_buffer(heic_resized)
    license_plates_info = get_license_plate(png_buffer)

    if license_plates_info.data is None:
        return "Not found any"

    vin_responses: list[VinResponse] = []
    for result in license_plates_info.data.results:
        print(result)
        plate = result.plate
        code = result.region.code
        if code.split("-")[0] == "us":
            code = code.split("-")[1].upper()
        else:
            return "not usa country"

        vin_response = lookup_plate(plate, code)

        if vin_response is None:
            return "Plate is invalid"

        vin_responses.append(vin_response)

    car_recognition = recognize_car(png_buffer)

    return {
        "license plates info": license_plates_info,
        "metadata": metadata_dict,
        "vin responses": vin_responses,
    }


@app.post("/license-plate-ocr/")
async def extract_license(image: UploadFile = File(...)):
    path = await save_to_disk(image, TMP_DIR)
    print("image saved to disk: ", path)

    ## Getting license plate from the image
    heic_image = open_heic_image(path)
    heic_resized = resize_image(heic_image)
    png_buffer = make_png_buffer(heic_resized)
    license_plates_info = get_license_plate(png_buffer)
    print(license_plates_info)
    json_data = jsonable_encoder(license_plates_info.data.results[0].plate)
    
    return JSONResponse(content=json_data)

@app.post("/recognize-car/")
async def recognize_car_api(image: UploadFile = File(...)):
    path = await save_to_disk(image, TMP_DIR)
    print("image saved to disk: ", path)

    ## Getting license plate from the image
    heic_image = open_heic_image(path)
    heic_resized = resize_image(heic_image)
    png_buffer = make_png_buffer(heic_resized)
    car_recognition = recognize_car(png_buffer)
    print(car_recognition)
    json_data = jsonable_encoder(car_recognition)
    
    return JSONResponse(content=json_data)

@app.post("/lookup-plate/")
async def lookup_plate(plate: str = Form(...), state_code: str = Form(...)):
    print(plate, state_code)
    vin_response = lookup_plate(plate, state_code)
    print(vin_response)
    json_data = jsonable_encoder(vin_response)
    
    return JSONResponse(content=json_data)