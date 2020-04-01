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
    link = request.get_json().get("link", "")
    size = request.get_json().get("size", "")
    uploaded_by = request.get_json().get("uid", "")
    uploaded_at = int(time.time())

    print(link, size, uploaded_by)

    if link == "":
        return "No link provided", 400
    if size == "":
        return "No size provided", 400
    if uploaded_by == "":
        return "No uid provided", 400

    csv_loader = requests.get(link, stream=True)

    features = []

    for line in csv_loader.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            features = decoded_line.split(',')
            break

    dataset_ref = db.reference('/datasets').push()
    dataset_ref.set({
        'features': features,
        'link': link,
        'size': size,
        'uploaded_by': uploaded_by,
        'uploaded_at': uploaded_at
    })

    user_ref = db.reference('/users/{}/datasets/{}'.format(uploaded_by, dataset_ref.key)).set(link)

    return jsonify({"features": features, "dataset_id": dataset_ref.key}), 200

    
    


@datasets_api.route("/datasets/<datasetid>", methods=["GET"])
def retrieve_dataset(datasetid):
    pass