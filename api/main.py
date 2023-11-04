import json
import os

import aiofiles
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

TMP_DIR = 'objects'

app = FastAPI()


app.get("/")(lambda: {"Hello": "World"})


async def save_to_disk(image, tmp_dir):
    # save the file
    path = os.path.join(tmp_dir, image.filename)
    async with aiofiles.open(path, 'wb') as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write
    return path


class ImageMetadata(BaseModel):
    lat: str
    long: str


@app.post("/upload/")
async def upload_image(
        metadata: str = Form(...),
        image: UploadFile = File(...)):
   
    metadata_dict = json.loads(metadata)
    print("inputted metadata: ", metadata_dict)

    path = await save_to_disk(image, TMP_DIR)
    print("image saved to disk: ", path)

    return {"filename": image.filename,
            "metadata": metadata_dict}
