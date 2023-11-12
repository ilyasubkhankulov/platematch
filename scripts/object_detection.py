import torch


def object_detection(img):
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
