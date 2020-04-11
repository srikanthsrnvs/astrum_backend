import json
import logging
import time

import pandas
import requests
from firebase_admin import auth, credentials, db, exceptions
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

datasets_api = Blueprint("datasets_api", __name__)


@datasets_api.route("/datasets", methods=["POST"])
def add_dataset():
    dataset_type = request.get_json().get("type", "")
    uploaded_by = request.get_json().get("uploaded_by", "")
    print(request.get_json().keys())
    user_snapshot = db.reference('/users/'+uploaded_by).get()
    if uploaded_by == "" or not user_snapshot:
        print("No such user exists "+uploaded_by)
        return "No user information provided", 400

    if dataset_type == "image_classification" or dataset_type == 'object_detection' or dataset_type == 'object_localization':
        file_upload = request.get_json().get("file", {})
        dataset_ref = db.reference('/datasets').push()
        dataset_ref.set({
            'uploaded_by': uploaded_by,
            'file': file_upload,
            'dataset_type': dataset_type
        })
        user_ref = db.reference(
            '/users/{}/datasets/{}'.format(uploaded_by, dataset_ref.key)).set('true')
        return jsonify({'dataset_id': dataset_ref.key, 'status': 'success'}), 200

    elif dataset_type == "structured_prediction":
        # csv_loader = requests.get(link, stream=True)

        # features = []

        # for line in csv_loader.iter_lines():
        #     if line:
        #         decoded_line = line.decode('utf-8')
        #         features = decoded_line.split(',')
        #         break
        pass

    elif dataset_type == 'structured_classification':
        pass

    elif dataset_type == "custom":
        pass

    else:
        return "No such dataset_type", 400


@datasets_api.route("/datasets/<datasetid>", methods=["GET"])
def retrieve_dataset(datasetid):
    pass
