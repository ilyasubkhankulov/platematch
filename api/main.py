import json
import os

import aiofiles
from lib.recognize_car import recognize_car
from lib.lookup_plate import VinResponse
from lib.image_preprocessing import make_png_buffer, open_heic_image, resize_image
from lib.license_plate_recognition import get_license_plate
from lib.lookup_plate import lookup_plate

# from lib.convert_image import heic_to_png_buffer
from constants import TMP_DIR
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel


app = FastAPI()


app.get("/")(lambda: {"Hello": "World"})


async def save_to_disk(image, tmp_dir):
    # save the file
    path = os.path.join(tmp_dir, image.filename)
    async with aiofiles.open(path, "wb") as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write
    return path


class ImageMetadata(BaseModel):
    lat: str
    long: str


@app.post("/upload/")
async def upload_image(metadata: str = Form(...), image: UploadFile = File(...)):
    metadata_dict = json.loads(metadata)
    print("inputted metadata: ", metadata_dict)

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
