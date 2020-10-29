from flask import Flask, request, redirect, render_template, Response
import os
from werkzeug.utils import secure_filename
from imutils.video import VideoStream
import imutils
import cv2

app = Flask(__name__, template_folder="template")
file_name = "faces"
app.config["IMAGE_UPLOADS"] = os.path.abspath(file_name)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/recognize-image", methods=["GET", "POST"])
def recognize_image():
    return render_template("recognize.html")


stream = VideoStream(src=0).start()


@app.route("/camera-recognize-image")
def camera_recognize_image():
    return render_template("camera.html")


@app.route("/video")
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    while True:
        frame = stream.read()
        frame = imutils.resize(frame, width=1000)
        (flag, encodedImage) = cv2.imencode(app.config["IMAGE_UPLOADS"], frame)
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
