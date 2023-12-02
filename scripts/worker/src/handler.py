import json
import tempfile
from pathlib import Path

import requests
import runpod
import torch
from ultralytics import YOLO

# Load a model from the filesystem
model = YOLO('/cache/yolov8n.pt')  # load a local model
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")

# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.


def object_detection(img_path):
    # Model
    # or yolov5n - yolov5x6, custom

    # Inference
    results = model(img_path)
    results_json_list = [json.loads(result.tojson()) for result in results]

    print('results_json_list', results_json_list)
    return results_json_list


def download_from_url(url):

    # Download the file from `url` and save it locally with a .jpg extension:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            # Return the path to the downloaded file with .jpg extension
            return Path(f.name)


def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    image_url = job_input.get('image_url')
    # print(image_url)
    image_path = download_from_url(image_url)
    # print(image_path)
    results = object_detection(image_path)

    return results


runpod.serverless.start({"handler": handler})
