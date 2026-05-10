from flask import Flask, render_template

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

BLOB_ENDPOINT = "https://colorqueue.blob.core.windows.net"
CONTAINER_NAME = "images"
MAX_IMAGE_COUNT = 9

app = Flask(__name__)

credential = DefaultAzureCredential()

blob_client = BlobServiceClient(account_url=BLOB_ENDPOINT, credential=credential)

@app.route("/")
def index():
    image_paths = []

    container_client = blob_client.get_container_client(CONTAINER_NAME)
    images = list(container_client.list_blobs())
    images.sort(key=lambda x: x.last_modified, reverse=True)
    for image in images[:MAX_IMAGE_COUNT]:
        image_paths.append(f"{BLOB_ENDPOINT}/{CONTAINER_NAME}/{image.name}")

    return render_template("index.html", image_paths=image_paths)
