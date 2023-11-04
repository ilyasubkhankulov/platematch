import json

from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


app.get("/")(lambda: {"Hello": "World"})


class ImageMetadata(BaseModel):
    lat: str
    long: str


@app.post("/upload/")
async def upload_image(metadata: str = Form(...), image: UploadFile = File(...)):
    # metadata_dict = metadata
    print(metadata)
    return {"filename": image.filename,
            "metadata": metadata}