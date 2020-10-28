from flask import Flask, request, redirect, render_template
from faceApp import *
import json
import os
from werkzeug.utils import secure_filename

IMAGE_UPLOADS = "faces/"
ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG"]


def allowed_image(filename):
    if not "." in filename:
        return False

    file_extension = filename.rsplit(".", 1)[1]

    if file_extension.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


app = Flask(__name__)



@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            print("Image saved")

            return redirect(request.url)
        else:
            print("That file extension is not allowed")
            return redirect(request.url)

    return render_template("webApp.html")


app.run(debug=True, port=8080)
