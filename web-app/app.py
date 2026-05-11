from os import urandom
from re import match

from flask import flash, Flask, redirect, render_template, request, url_for

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

BLOB_ENDPOINT = "https://colorqueue.blob.core.windows.net"
CONTAINER_NAME = "images"
MAX_IMAGE_COUNT = 9

app = Flask(__name__)
app.secret_key = urandom(24)

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

@app.route("/add", methods=["POST"])
def add():
    color = request.form.get("color")
    if match(r'^#[0-9a-fA-F]{6}$', color):
        flash(f"Success: Color queued, refresh in a few seconds.")
    else:
        flash("Error: Invalid color format.")

    return redirect(url_for("index"))
