import gc
import json
import os
import pickle
from datetime import datetime

import astral
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from astral.sun import sun
from object_detection import object_detection
from pytz import timezone
from tqdm import tqdm

image_dir = 'tmp'


image_files = [os.path.join(image_dir, f)
               for f in os.listdir(image_dir) if f.endswith('.jpg')]
image_files_iter = iter(image_files)

output_list = []

image_files_in_output_list = [output['image_file'] for output in output_list]

for image_file in tqdm(image_files_iter):
    if image_file not in image_files_in_output_list:
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

for item in tqdm(output_list):

    detection_results = json.loads(item['detection_result'])
    # print('detection_results', detection_results)
    # Remove heavily overlapping bounding boxes, keeping the one with higher confidence
    i = 0
    while i < len(detection_results['name']):
        j = i + 1
        while j < len(detection_results['name']):
            # Calculate the intersection over union (IoU) of the two bounding boxes
            # print(detection_results)
            if str(i) in detection_results['xmin'] and str(j) in detection_results['xmin']:
                xi1 = max(detection_results['xmin'][str(i)],
                          detection_results['xmin'][str(j)])
                yi1 = max(detection_results['ymin'][str(i)],
                          detection_results['ymin'][str(j)])
                xi2 = min(detection_results['xmax'][str(i)],
                          detection_results['xmax'][str(j)])
                yi2 = min(detection_results['ymax'][str(i)],
                          detection_results['ymax'][str(j)])
                inter_area = max(0, xi2 - xi1 + 1) * max(0, yi2 - yi1 + 1)
                box1_area = (detection_results['xmax'][str(i)] - detection_results['xmin'][str(i)] + 1) * (
                    detection_results['ymax'][str(i)] - detection_results['ymin'][str(i)] + 1)
                box2_area = (detection_results['xmax'][str(j)] - detection_results['xmin'][str(j)] + 1) * (
                    detection_results['ymax'][str(j)] - detection_results['ymin'][str(j)] + 1)
                iou = inter_area / float(box1_area + box2_area - inter_area)

                # If the IoU is greater than 0.5, they are heavily overlapping
                if iou > 0.5:
                    print(
                        f"Processing image {item['image_file']}")
                    print(iou)
                    print("detection_results['confidence'][str(i)]",
                          detection_results['confidence'][str(i)])
                    print("detection_results['confidence'][str(j)]",
                          detection_results['confidence'][str(j)])
                    print(
                        f"Removed bounding box for {detection_results} in image {item['image_file']}")
                    # Remove the bounding box with lower confidence
                    if detection_results['confidence'][str(i)] > detection_results['confidence'][str(j)]:
                        detection_results['name'].pop(str(j))
                        detection_results['xmin'].pop(str(j))
                        detection_results['ymin'].pop(str(j))
                        detection_results['xmax'].pop(str(j))
                        detection_results['ymax'].pop(str(j))
                        detection_results['confidence'].pop(str(j))
                    else:

                        detection_results['name'].pop(str(i))
                        detection_results['xmin'].pop(str(i))
                        detection_results['ymin'].pop(str(i))
                        detection_results['xmax'].pop(str(i))
                        detection_results['ymax'].pop(str(i))
                        detection_results['confidence'].pop(str(i))

                        i -= 1
                    break
            j += 1
        i += 1

with open('output_list.pkl', 'wb') as f:
    pickle.dump(output_list, f)

with open('output_list.pkl', 'rb') as f:
    output_list = pickle.load(f)


location = astral.LocationInfo(
    "Oakland", "USA", "US/Pacific", 37.8044, -122.2712
)

for output in output_list:
    filename = output['image_file'].split('/')[-1]
    camera_name, date, hour, minutes = filename.split('_')[2], filename.split(
        '_')[3], filename.split('_')[6], filename.split('_')[7].split('.')[0]
    seconds = filename.split('_')[7].split('.')[1][0:2]
    year, month, day = date.split('-')
    output['camera_name'] = camera_name
    output['datetime'] = datetime(int(year), int(month), int(
        day), int(hour), int(minutes), int(seconds))
    # Use astral library to get sun information for the specific date and location
    s = sun(location.observer, date=output['datetime'].date(
    ), tzinfo=timezone('US/Pacific'))

    # Classify the lighting based on the sun information
    if s['dawn'].time() <= output['datetime'].time() < s['sunrise'].time():
        output['lighting'] = 'dawn'
    elif s['sunrise'].time() <= output['datetime'].time() < s['sunset'].time():
        output['lighting'] = 'day'
    elif s['sunset'].time() <= output['datetime'].time() < s['dusk'].time():
        output['lighting'] = 'dusk'
    else:
        output['lighting'] = 'night'

for output in output_list:
    print(output['image_file'], output['lighting'])
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

        # Draw bounding box
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        # Calculate label size and position
        (label_width, label_height), baseline = cv2.getTextSize(
            label_with_confidence, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        label_ymin = max(ymin, label_height + 10)
        # Draw black background rectangle
        cv2.rectangle(img, (xmin, label_ymin - label_height - 10), (xmin +
                      label_width, label_ymin + baseline - 10), (0, 0, 0), cv2.FILLED)
        # Add label with confidence on the black background
        cv2.putText(img, label_with_confidence, (xmin, label_ymin - 7),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Add 'lighting' label in the upper right hand side
    lighting_label = output['lighting']
    cv2.putText(img, lighting_label, (img.shape[1] - 100, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Save the image in the 'tmp_labeled' directory
    labeled_image_file = os.path.join(
        'tmp_labeled', output['image_file'].split('/')[-1])
    cv2.imwrite(labeled_image_file, img)

# df = pd.DataFrame(output_list)

# Get simple counts of events based on camera_name from output_list
camera_counts = {}
for output in output_list:
    camera_name = output['camera_name']
    if camera_name not in camera_counts:
        camera_counts[camera_name] = 0
    camera_counts[camera_name] += 1


object_dict = {}
for output in output_list:
    detection_results = json.loads(output['detection_result'])
    for i in range(len(detection_results['name'])):
        object_name = detection_results['name'][str(i)]
        if object_name not in object_dict:
            object_dict[object_name] = []
        object_dict[object_name].append(output)

# Create a dictionary to store confidence intervals
confidence_buckets = {'0-25%': [],
                      '26-50%': [], '51-75%': [], '76-100%': []}

# Iterate over the object dictionary
for object_name, outputs in object_dict.items():
    if object_name in ['car', 'truck']:
        for output in outputs:
            detection_results = json.loads(output['detection_result'])
            for i in range(len(detection_results['name'])):
                if detection_results['name'][str(i)] == object_name:
                    confidence = int(
                        float(detection_results['confidence'][str(i)]) * 100)
                    if confidence <= 25:
                        bucket = '0-25%'
                    elif confidence <= 50:
                        bucket = '26-50%'
                    elif confidence <= 75:
                        bucket = '51-75%'
                    else:
                        bucket = '76-100%'
                    confidence_buckets[bucket].append(
                        (output['lighting'], output['datetime'], output['camera_name'], output['image_file'].split('/')[-1].split('.')[0]))
# Create a dictionary to store the count of each bucket per day
bucket_counts_per_day = {}
for bucket, data in confidence_buckets.items():
    df = pd.DataFrame(
        data, columns=['lighting', 'datetime', 'camera_name', 'image_filename'])
    df['date'] = pd.to_datetime(df['datetime'])
    df['day_of_week'] = df['date'].dt.day_name()
    # Add date in unixtime for sorting later
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    df.set_index('day_of_week', inplace=True)
    bucket_counts = df.groupby(['day_of_week', 'date_str', 'lighting']).size()
    bucket_counts_per_day[bucket] = bucket_counts

bucket_counts_df = pd.DataFrame(bucket_counts_per_day)
bucket_counts_df = bucket_counts_df.fillna(0)
bucket_counts_df = bucket_counts_df.stack().reset_index()
bucket_counts_df.columns = ['day_of_week', 'date_str',
                            'lighting', 'bucket', 'count']

# Calculate the total count for each day_of_week and lighting
total_counts = bucket_counts_df.groupby(['day_of_week', 'lighting'])[
    'count'].sum().reset_index()
total_counts.columns = ['day_of_week', 'lighting', 'total']

# Merge the total counts back to the original dataframe
bucket_counts_df = pd.merge(bucket_counts_df, total_counts, on=[
                            'day_of_week', 'lighting'])

# Calculate the percentage
bucket_counts_df['percentage'] = bucket_counts_df['count'] / \
    bucket_counts_df['total'] * 100

bucket_counts_df = bucket_counts_df[bucket_counts_df['date_str']
                                    != '2023-11-11']

bucket_counts_df = bucket_counts_df[bucket_counts_df['date_str']
                                    != '2023-11-07']


sns.set(style="whitegrid")
if 'percentage' in bucket_counts_df.columns:
    # Pivot the dataframe to create a 100% stacked bar chart
    pivot_df = bucket_counts_df.pivot_table(
        index=['lighting', 'date_str'], columns='bucket', values='percentage')
    pivot_df = pivot_df.div(pivot_df.sum(axis=1), axis=0).multiply(100)
    # Sort the dataframe by date_str and lighting
    # pivot_df = pivot_df.sort_values(by=['date_str', 'lighting'])
    plot = pivot_df.plot(kind='bar', stacked=True, colormap='RdYlGn')
    # Rotate x-axis labels for better visibility and adjust for auto-fit
    labels = bucket_counts_df['lighting'] + ', ' + bucket_counts_df['date_str']
    sorted_labels = sorted(labels.unique())
    plt.xticks(ticks=range(len(sorted_labels)),
               rotation=45, ha='right', labels=sorted_labels)
    plt.tight_layout()
    # Move the legend outside the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
else:
    print("Error: 'percentage' column not found in the dataframe.")
plt.title('Confidence Distribution of Cars and Trucks by Day and by Sun Phase')
plt.savefig('Confidence_Distribution_per_Day_of_Week_and_Lighting.png',
            bbox_inches='tight')
plt.close()

# create a normalized list of car and truck objects from the output_list
# crop each image to the bounding box of the car or truck
# save the cropped image to a new directory
# create a list of the cropped images
# run the cropped images through the license plate recognition model
# run the cropped images through the car recognition model
# for each recognized plate, run through DMV database
# create a funnel visualization for performance of each step
