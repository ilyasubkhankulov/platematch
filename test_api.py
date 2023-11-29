import json

import requests

# Prepare metadata
metadata = json.dumps({'lat': '123', 'long': '456'})
# convert dict to str

# Prepare headers
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

file_path = './scripts/test-images/_files_MailCam_2023-11-09_001_jpg_12_51.14[M][0@0][0].jpg'

with open(file_path, 'rb') as f:
    files = {'upload_file': f.read()}

# Open the file in binary
image_file = open(file_path, 'rb')

# Make POST request with file and metadata
response = requests.post(
    'http://localhost:8090/upload/',
    files={'image': image_file},
    data={'lat': '123', 'long': '456'}
)

# Close the file
image_file.close()


print(response.json())
