import json

import requests

# Prepare metadata
metadata = {'lat': '123', 'long': '456'}

# Prepare headers 
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

file_path = '/Users/ilya/Desktop/screenshots/lexus.png'

with open(file_path, 'rb') as f:
    files = {'upload_file': f.read()}

# Open the file in binary
image_file = open(file_path, 'rb')

# Make POST request with file and metadata
response = requests.post(
    'http://localhost:8000/upload/',
    files={'image': image_file},
    data={'metadata': metadata}
)

# Close the file
image_file.close()


print(response.json())