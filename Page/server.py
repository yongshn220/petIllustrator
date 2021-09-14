# -*- coding: utf-8 -*-
from logging import error
from re import DEBUG
from flask import Flask, render_template, request, flash, redirect, url_for
from flask import send_from_directory
from main import Main
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, exc
import cv2
import numpy as np
import os

COVER_FOLDER = os.path.join('static', 'image')
RESULT_FOLDER = "C:\Github\Python\PetIllustrator\Page\images\Result"


main = Main()
app = Flask(__name__)
app.config['COVER_FOLDER'] = COVER_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route("/", methods=['GET', 'POST'])
def index():


    if request.method == 'GET':
        return render_template('index.html')


@app.route("/download", methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        return render_template('index.html')
        
    if request.method == "POST":
        userId = request.form['userId']

        s = Serializer('WEBSITE_SECRET_KEY', 60*1)
        token = s.dumps({'user_id': userId}).decode('utf-8') # encode user id  

        files = request.files.getlist('image-files')
        
        decide_img = decode(files[0])
        result_img = main.convert(decide_img)

        #save result image
        cv2.imwrite('./Page/images/Result/' + userId +'.png', result_img)
        #save cover image (preview)
        cv2.imwrite('./Page/static/image/coverImage.png', result_img)
        #address for cover image (frontend)
        preview_img = os.path.join(app.config['COVER_FOLDER'], 'coverImage.png')
        return render_template('download.html', resImg=preview_img, token=token)


@app.route("/<token>", methods=['GET'])
def downloadFile(token):
    s = Serializer('WEBSITE_SECRET_KEY')
    
    try:
        data = s.loads(token)
    except:
        return 'This is an invalid or expired URL, please generate a new one!'

    userId = data['user_id']

    if not userId:
        return redirect(url_for('index'))
    
    filename = userId + ".png"
    
    try:
        return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)

    except FileNotFoundError:
        os.abort(404)


def decode(file):
    np_img = np.fromfile(file, np.uint8)
    ori_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    return ori_img


if __name__ == '__main__':
    app.run(debug=True)
