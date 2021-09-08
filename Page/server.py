# -*- coding: utf-8 -*-
from re import DEBUG
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from main import Main
import cv2
import numpy as np
import os


RESULT_FOLDER = os.path.join('static', 'image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = RESULT_FOLDER

@app.route("/", methods=['GET', 'POST'])
def index():
    testMsg = "Test"
    if request.method == 'GET':
        
        return render_template('index.html')


@app.route("/download", methods=['GET', 'POST'])
def index2():
    if request.method == 'GET':
        return render_template('index.html')
        
    if request.method == "POST":
        files = request.files.getlist('image-files')
        
        np_img = np.fromfile(files[0], np.uint8)

        ori_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        main = Main()
        
        result_img = main.convert(ori_img)
        cv2.imwrite('./Page/static/image/resultImage.png', result_img)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'resultImage.png')
        return render_template('index.html', resImg=full_filename)



if __name__ == '__main__':
    app.run(debug=True)
