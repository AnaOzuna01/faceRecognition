from flask import Flask, request, redirect, render_template
import os
from faceApp import *
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="template")
file_name = "faces"
app.config["IMAGE_UPLOADS"] = os.path.abspath(file_name)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):
    if not "." in filename:
        return False
    extension_file = filename.rsplit(".", 1)[1]
    if extension_file.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:

            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("File exceeded maximum size")
                return redirect(request.url)

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

            print("Image saved")

            return redirect(request.url)

    return render_template("webApp.html")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
