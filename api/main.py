import json
import os

import aiofiles
from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


app.get("/")(lambda: {"Hello": "World"})


class ImageMetadata(BaseModel):
    lat: str
    long: str

@app.post("/upload/")
async def upload_image(metadata: str = Form(...), image: UploadFile = File(...)):
    metadata_dict = json.loads(metadata)
    print(metadata_dict)

    # save the file
    path = os.path.join('objects', image.filename)
    async with aiofiles.open(path, 'wb') as out_file:
        content = await image.read()  # async read
        await out_file.write(content)  # async write

    return {"filename": image.filename,
            "metadata": metadata_dict, 
            "path": path}
