import io
from PIL import Image
from pillow_heif import register_heif_opener, HeifImage


def open_heic_image(heic_path):
    register_heif_opener()
    heic_image = Image.open(heic_path)
    return heic_image


def make_png_buffer(image):
    png_buffer = io.BytesIO()
    image.save(png_buffer, format="PNG")
    png_buffer.seek(0)
    return png_buffer


# GET AND RETURNS PIL IMAGE
def resize_image(image):
    width, height = image.size
    if width > 1024 or height > 768:
        ratio = min(1024.0 / width, 768.0 / height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    return image
