from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import time
import requests
import json
import logging
from firebase_admin import auth, db, exceptions, credentials
import pandas


datasets_api = Blueprint("datasets_api", __name__)


@datasets_api.route("/datasets", methods=["POST"])
def add_dataset():
    dataset_type = request.get_json().get("type", "")
    uploaded_by = request.get_json().get("uploaded_by", "")

    user_snapshot = db.reference('/users/'+uploaded_by).get()
    if uploaded_by == "" or not user_snapshot.val():
        return "No user information provided", 400

    if dataset_type == "image_classification":
        child_datasets = request.get_json().get("child_datasets", {})

        if child_datasets == {}:
            return "No child datasets provided", 400

        dataset_ref = db.reference('/datasets').push()
        dataset_ref.set({
            'uploaded_by': uploaded_by,
            'child_datasets': child_datasets,
            'dataset_type': dataset_type
        })

        user_ref = db.reference('/users/{}/datasets/{}'.format(uploaded_by, dataset_ref.key)).set('true')
        return "Datasets stored", 200

    else if dataset_type == "structured_prediction":
        # csv_loader = requests.get(link, stream=True)

        # features = []

        # for line in csv_loader.iter_lines():
        #     if line:
        #         decoded_line = line.decode('utf-8')
        #         features = decoded_line.split(',')
        #         break
        pass

    else if dataset_type == 'structured_classification':
        pass

    else if dataset_type == "custom":
        pass

    else:
        return "No such dataset_type", 400


@datasets_api.route("/datasets/<datasetid>", methods=["GET"])
def retrieve_dataset(datasetid):
    pass