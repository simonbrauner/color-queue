from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    image_paths = []
    for _ in range(9):
        image_paths.append("/static/a.png")

    return render_template("index.html", image_paths=image_paths)
