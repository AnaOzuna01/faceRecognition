from flask import Flask, request, redirect, render_template
import os
from faceApp import *
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="template")
file_name = "faces"
app.config["IMAGE_UPLOADS"] = os.path.abspath(file_name)


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image saved")
            return redirect(request.url)
    return render_template("webApp.html")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
