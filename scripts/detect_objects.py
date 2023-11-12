import gc
import json
import os
import pickle
from datetime import datetime

import cv2
import pandas as pd
from object_detection import object_detection
from tqdm import tqdm

image_dir = 'tmp'


image_files = [os.path.join(image_dir, f)
               for f in os.listdir(image_dir) if f.endswith('.jpg')]
image_files_iter = iter(image_files)

output_list = []


for image_file in tqdm(image_files_iter):
    detection_result = object_detection(image_file)
    detection_result_json = detection_result.pandas().xyxy[0].to_json()
    print('image_file', image_file)
    print('detection_result_json', detection_result_json)
    output_list.append({
        'image_file': image_file,
        'detection_result': detection_result_json
    })
    # Explicitly delete the detection_result and call the garbage collector
    del detection_result
    gc.collect()


with open('output_list.pkl', 'wb') as f:
    pickle.dump(output_list, f)


# _files_NorthStreetCam_2023-11-10_001_jpg_16_20.23[M][0@0][0].jpg
for output in output_list:
    filename = output['image_file'].split('/')[-1]
    camera_name, date, hour, minutes = filename.split('_')[2], filename.split('_')[
        3], filename.split('_')[6], filename.split('_')[7]
    year, month, day = date.split('-')
    minute, second = minutes.split('.')[0], minutes.split('.')[1][0:2]
    output['camera_name'] = camera_name
    output['datetime'] = datetime(int(year), int(month), int(
        day), int(hour), int(minute), int(second))

for output in output_list:
    # Load the image
    img = cv2.imread(output['image_file'])

    # Load the detection results
    detection_results = json.loads(output['detection_result'])

    # Draw bounding boxes and labels on the image
    for i in range(len(detection_results['name'])):
        xmin = int(detection_results['xmin'][str(i)])
        ymin = int(detection_results['ymin'][str(i)])
        xmax = int(detection_results['xmax'][str(i)])
        ymax = int(detection_results['ymax'][str(i)])
        label = detection_results['name'][str(i)]
        # Convert confidence to percentage
        confidence = int(float(detection_results['confidence'][str(i)]) * 100)
        # Add confidence to label
        label_with_confidence = f"{label} {confidence}%"

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(img, label_with_confidence, (xmin, ymin-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)  # Increased font size and high contrast color

    # Save the image in the 'tmp_labeled' directory
    labeled_image_file = os.path.join(
        'tmp_labeled', output['image_file'].split('/')[-1])
    cv2.imwrite(labeled_image_file, img)

# df = pd.DataFrame(output_list)

object_dict = {}
for output in output_list:
    detection_results = json.loads(output['detection_result'])
    for i in range(len(detection_results['name'])):
        object_name = detection_results['name'][str(i)]
        if object_name not in object_dict:
            object_dict[object_name] = []
        object_dict[object_name].append(output)
