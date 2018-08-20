import flask
from flask import Flask, request, make_response, jsonify
import json
import werkzeug
from datetime import datetime
import os
from google.cloud import storage

UPLOAD_FOLDER = 'upload/'
FILE_ID_AT_HTML = 'file'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024


    
@app.after_request
def after_request(response):
            response.headers.add('Access-Control-Allow-Origin','http://localhost:4212')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,Origin')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials','true')
            return response

@app.route('/')
def index():
    return "work!!"

@app.route('/*', methods=['OPTIONS'])
def opt():
    return result(200,"ok")


import auto_ml_predict
import json
@app.route('/predict', methods=['POST'])
def predict():
            if request.headers['Content-Type'] != 'application/json':
                        print(request.headers['Content-Type'])
                        return result(500, "content-type invalid")

            print request.json["image_name"]
            img_file_name = request.json["image_name"]
            content = auto_ml_predict.img_open(img_file_name)
            score, display_name = auto_ml_predict.get_prediction(content)

            return result(200, [{'score': score, 'display_name':display_name}] )


@app.route('/upload', methods=['POST'])
def upload():
    if FILE_ID_AT_HTML not in request.files:
        return result(500, 'uploadfile not found')
        
    upload_file = request.files[FILE_ID_AT_HTML]
    fileName = upload_file.filename
    if '' == fileName:
        return result(500, 'filename must not empty.')

    saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
        + werkzeug.utils.secure_filename(fileName)
    upload_file.save(os.path.join(UPLOAD_FOLDER, saveFileName))
    return result(200, saveFileName)


@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'file size is overed.'


def result(status_code, msg):
    return make_response(jsonify({'status':status_code, 'message':msg})) 

if __name__ == '__main__':
    from google.cloud import storage
    app.run(host='0.0.0.0', port=5000, debug=True)

