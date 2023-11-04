import os
from pathlib import Path

from constants import TMP_DIR
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def heic_to_png(input_path):
    # Load the heic image
    image = Image.open(input_path)

    # get filename w/o extension
    filename = Path(input_path).stem
    print(filename)

    output_path = os.path.join(TMP_DIR, f"{filename}.png")
    # Convert the image to png
    image.save(output_path)

    return output_path


# Restrictions
# File Upload Error - Payload Too Large
# File size must be lower than 3MB.
# Recommended image resolution: 1024×768.
# Recommended orientation: portrait.
# Vehicle should be at least 15% of the total image area.
# License plate should be readable by a human.
