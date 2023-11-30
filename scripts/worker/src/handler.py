""" Example handler file. """
import tempfile
from pathlib import Path

import requests
import runpod
import torch

model = torch.hub.load("ultralytics/yolov5", "yolov5s")
# If your handler runs inference on a model, load the model here.
# You will want models to be loaded into memory before starting serverless.


def object_detection(img_path):
    # Model
    # or yolov5n - yolov5x6, custom

    # Inference
    results = model(img_path)

    print(results.print)
    print(results.xyxy[0])
    # Results
    # results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
    # Return list of objects detected with bounding boxes
    return results  # img1 predictions (tensor)


def download_from_url(url):

    # Download the file from `url` and save it locally under `file_name`:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            # Return the path to the downloaded file
            return Path(f.name)


def handler(job):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    image_url = job_input.get('image_url')

    image_path = download_from_url(image_url)

    results = object_detection(image_path)

    return results


runpod.serverless.start({"handler": handler})
