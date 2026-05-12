from os import urandom
from re import match

from flask import flash, Flask, redirect, render_template, request, url_for
from requests import get

from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
from azure.identity import DefaultAzureCredential

BLOB_ENDPOINT = "https://colorqueue.blob.core.windows.net"
CONTAINER_NAME = "images"

QUEUE_ENDPOINT = "https://colorqueue.queue.core.windows.net"
QUEUE_NAME = "colors"

FUNCTION_URL = "https://color-queue2.azurewebsites.net/api/draw"

MAX_IMAGE_COUNT = 9

app = Flask(__name__)
app.secret_key = urandom(24)

credential = DefaultAzureCredential()

blob_client = BlobServiceClient(account_url=BLOB_ENDPOINT, credential=credential)

queue_client = QueueServiceClient(account_url=QUEUE_ENDPOINT, credential=credential)

@app.route("/")
def index():
    image_paths = []

    container_client = blob_client.get_container_client(CONTAINER_NAME)
    images = list(container_client.list_blobs())
    images.sort(key=lambda x: x.last_modified, reverse=True)
    for image in images[:MAX_IMAGE_COUNT]:
        image_paths.append(f"{BLOB_ENDPOINT}/{CONTAINER_NAME}/{image.name}")

    # Proof that the queue at least receives the messages.
    queue = queue_client.get_queue_client(QUEUE_NAME)
    properties = queue.get_queue_properties()
    message_count = properties.approximate_message_count

    return render_template("index.html", image_paths=image_paths, message_count=message_count)

@app.route("/add", methods=["POST"])
def add():
    color = request.form.get("color")
    if match(r'^#[0-9a-fA-F]{6}$', color):
        queue = queue_client.get_queue_client(QUEUE_NAME)
        queue.send_message(color)

        # Queue does not work, HTTP request as a workaround.
        response = get(FUNCTION_URL, params={"color": color}, timeout=5)
        if response.status_code == 201:
            flash("Success: Color added.")
        else:
            flash(f"Error: Drawing failed: {response.text}")
    else:
        flash("Error: Invalid color format.")

    return redirect(url_for("index"))
