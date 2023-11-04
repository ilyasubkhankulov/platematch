import json
import os
from typing import Optional, Union

import aiofiles

# from lib.convert_image import heic_to_png_buffer
from constants import TMP_DIR
from fastapi import FastAPI, File, Form, UploadFile
from lib.convert_image import heic_to_png
from pydantic import BaseModel

app = FastAPI()


app.get("/")(lambda: {"Hello": "World"})


async def save_to_disk(image, tmp_dir):
    # save the file
    path = os.path.join(tmp_dir, image.filename)
    async with aiofiles.open(path, 'wb') as out_file:
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

    png_location = heic_to_png(path)

    return {"filename": png_location,
            "metadata": metadata_dict}
