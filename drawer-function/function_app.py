from io import BytesIO
from re import match

from PIL import Image

import azure.functions as func

QUEUE_NAME = "colors"

app = func.FunctionApp()

IMAGE_SIZE=(100, 100)

@app.route(route="draw", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_output(arg_name="outputblob", path="images/{rand-guid}.png", connection="AzureWebJobsStorage")
def draw_square(req: func.HttpRequest, outputblob: func.Out[bytes]) -> func.HttpResponse:
    color = req.params.get('color')

    if not color:
        return func.HttpResponse("Missing 'color' parameter.", status_code=400)

    if not match(r'^#[0-9a-fA-F]{6}$', color):
        return func.HttpResponse("Wrong format of 'color' parameter.", status_code=400)

    img = Image.new('RGB', IMAGE_SIZE, color=color)
    buffer = BytesIO()
    img.save(buffer, format="png")

    outputblob.set(buffer.getvalue())

    return func.HttpResponse(f"Image created with color: {color}", status_code=201)
