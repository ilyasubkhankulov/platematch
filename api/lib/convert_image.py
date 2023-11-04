import io

import pyheif
from PIL import Image


def heic_to_png_buffer(heic_path):
    heif_file = pyheif.read(heic_path)
    if heif_file.size > 3000000:
        raise Exception("File size must be lower than 3MB.")
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()



# Restrictions
# File Upload Error - Payload Too Large
# File size must be lower than 3MB.
# Recommended image resolution: 1024×768.
# Recommended orientation: portrait.
# Vehicle should be at least 15% of the total image area.
# License plate should be readable by a human.
