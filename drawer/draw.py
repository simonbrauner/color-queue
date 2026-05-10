from uuid import uuid4

from PIL import Image

IMAGE_SIZE=(100, 100)

def draw_square(color):
    img = Image.new('RGB', IMAGE_SIZE, color=color)
    img.save(f"{uuid4()}.png")
