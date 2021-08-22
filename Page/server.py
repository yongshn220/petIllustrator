# -*- coding: utf-8 -*-
from re import DEBUG
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == "POST":
        files = request.files.getlist('image-files')

        num = 'a'
        for file in files:
            file.save('c:/Github/Python/FCN/Images/' + num + secure_filename(file.filename))
            num = num+'a'

        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
