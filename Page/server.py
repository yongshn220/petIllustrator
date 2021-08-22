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
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == "POST":
        files = request.files.getlist('image-files')

        np_img = np.fromfile(files[0], np.uint8)

        ori_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        bg_img = cv2.imread('./images/Background/Background-white.jpg', cv2.IMREAD_COLOR)
        cv2.imshow('test', bg_img)
        cv2.waitKey(0)
        #main = Main(ori_img, bg_img)   
        
        #main.convert()

        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
