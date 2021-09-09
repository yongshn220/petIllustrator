# -*- coding: utf-8 -*-
from re import DEBUG
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from main import Main
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import cv2
import numpy as np
import os


RESULT_FOLDER = os.path.join('static', 'image')

main = Main()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = RESULT_FOLDER

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route("/download", methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        return render_template('index.html')
        
    if request.method == "POST":
        token = request.form['token']

        s = Serializer('WEBSITE_SECRET_KEY', 60*30) # 60 secs by 30 mins
        token = s.dumps({'user_id': token}).decode('utf-8') # encode user id  

        files = request.files.getlist('image-files')
        
        decide_img = decode(files[0])
        result_img = main.convert(decide_img)

        cv2.imwrite('./Page/static/image/resultImage.png', result_img)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'resultImage.png')
        return render_template('download.html', resImg=full_filename, token=token)


@app.route("/download/<token>")
def downloadFile():
    return


def decode(file):
    np_img = np.fromfile(file, np.uint8)
    ori_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    return ori_img


if __name__ == '__main__':
    app.run(debug=True)
