import sys
import re
import json
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

FILE_PATH = "upload/"
PROJECT_ID = "sharp-respect-182803"
MODEL_ID = "ICN7958425307524780765"
KEY_FILE="key/sharp-respect-182803-30d43dc600fd.json"


def get_prediction(img_file):
    if img_file is None:
        print("img file is None")
        return error_result()

    prediction_client = automl_v1beta1.PredictionServiceClient()
    prediction_client = prediction_client.from_service_account_json(KEY_FILE)
  
    name = 'projects/{}/locations/us-central1/models/{}'.format(PROJECT_ID, MODEL_ID)
    payload = {'image': {'image_bytes': img_file }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    score, display_name = __request_parser(request)
    return score, display_name


def error_result():
    score = -1
    display_name = ""
    return score, display_name
    
def __request_parser(request):
    if len(request.payload) != 0:
        score = request.payload[0].classification.score
        display_name = str(request.payload[0].display_name)
        return score, display_name
    else:
        print("payload length is 0")
        return error_result()
    

    

def img_open(file_name):
    try:
        with open(FILE_PATH + file_name, 'rb') as ff:
            content = ff.read()
    except IOError:
        content = None
    return content    

if __name__ == '__main__':
    file_name = sys.argv[1]
    content = img_open(file_name)
    print get_prediction(content)


