import os

import requests
import torch
from dotenv import load_dotenv

load_dotenv()
RUNPOD_API_KEY = os.getenv('RUNPOD_API_KEY')
RUNPOD_API_URL = os.getenv('RUNPOD_API_URL')


def object_detection_runpod(img_url):
    input = {
        "input": {
            "image_url": img_url
        }
    }

    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    response = requests.post(RUNPOD_API_URL, headers=headers, json=input)

    print(response)
    print(response.json())
    return response.json()


def object_detection_local(img):
    # Model
    # or yolov5n - yolov5x6, custom
    model = torch.hub.load("ultralytics/yolov5", "yolov5s")

    # Inference
    results = model(img)

    print(results.print)
    print(results.xyxy[0])
    # Results
    # results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
    # Return list of objects detected with bounding boxes
    return results  # img1 predictions (tensor)
