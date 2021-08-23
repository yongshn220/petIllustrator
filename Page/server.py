# -*- coding: utf-8 -*-
from re import DEBUG
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from main import Main
import cv2
import numpy as np

app = Flask(__name__)

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

        main = Main(ori_img)
        
        result_img = main.convert()
        cv2.imwrite('resimg.png', result_img)
        testMsg = "Test2"
        return render_template('index2.html', testMsg = testMsg)



if __name__ == '__main__':
    app.run(debug=True)
