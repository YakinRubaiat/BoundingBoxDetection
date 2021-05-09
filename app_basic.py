import os
from uuid import uuid4
from flask import Flask, render_template, request,send_from_directory
import tensorflow as tf
global graph,model
graph = tf.get_default_graph()
import detection


result = 0

ml = detection.detectp()
     
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Image folder 
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    
    if not os.path.isdir(target):
            os.mkdir(target)

    print(request.files.getlist("file"))

    for upload in request.files.getlist("file"):

        destination = "/".join([target, 'X_ray.png'])
        
        upload.save(destination)
    
    result = ml.detect(destination)
    

    return render_template("complete.html",result=round(result*100,3))

@app.route("/upload")
def send_image():
    return send_from_directory("images", "heatmap.png")

if __name__ == "__main__":
    app.run(port=80)