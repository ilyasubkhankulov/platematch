import io
from PIL import Image
from pillow_heif import register_heif_opener, HeifImage


def heic_to_png_buffer(heic_path):
    register_heif_opener()
    heic_image = Image.open(heic_path)
    png_buffer = io.BytesIO()
    heic_image.save(png_buffer, format="PNG")
    png_buffer.seek(0)
    return png_buffer


Image
