import json
import uuid
from flask import Flask, request, render_template
from faceApp import *

UPLOAD_FOLDER = "/faces"

app = Flask(__name__, template_folder="template")

@app.route("/", methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename': f_name})
    return render_template("webApp.html")


if __name__ == '__main__':
   app.run(debug = True, port = 8080)
