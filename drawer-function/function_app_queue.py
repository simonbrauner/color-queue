from io import BytesIO

from PIL import Image

import azure.functions as func

QUEUE_NAME = "colors"

app = func.FunctionApp()

IMAGE_SIZE=(100, 100)

@app.queue_trigger(arg_name="msg", queue_name="colors", connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob", path="images/{rand-guid}.png", connection="AzureWebJobsStorage")
def draw_square(msg: func.QueueMessage, outputblob: func.Out[bytes]):
    color = msg.get_body().decode('utf-8')

    img = Image.new('RGB', IMAGE_SIZE, color=color)
    buffer = BytesIO()
    img.save(buffer, format="png")

    outputblob.set(buffer.getvalue())
