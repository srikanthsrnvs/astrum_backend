import json
import logging
import time
import requests
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build

from firebase_admin import auth, credentials, db, exceptions
from flask import Blueprint, jsonify, request

from paths.helpers import url, create_http_body, create_startup_script

jobs_api = Blueprint("jobs_api", __name__)


@jobs_api.route("/jobs", methods=['POST'])
def create_job():
    job_type = request.get_json().get("type", "")
    dataset = request.get_json().get("dataset", "")
    created_by = request.get_json().get("created_by")
    created_at = request.get_json().get("created_at")

    user_ref = db.reference('/users/'+created_by).get()

    if created_by == "" or not user_ref:
        return "No such userid exists", 400

    if job_type == 'image_classification':
        dataset_data = db.reference('/datasets/'+dataset).get()
        urls = []
        for child in dataset_data['child_datasets']:
            urls.append(child['link'])
        
        job_ref = db.reference('/jobs').push({
            'created_by': created_by,
            'created_at': created_at,
            'type': job_type,
            'dataset': dataset
        })
        credentials = GoogleCredentials.get_application_default()
        service = build('compute', 'v1', credentials=credentials)

        project = 'astrumdashboard'
        zone = 'us-central1-a'
        job_id = job_ref.key.lower()
        body = create_http_body(create_startup_script(urls, job_id), job_id)

        req = service.instances().insert(project=project, zone=zone, body=body)
        response = req.execute()
        print(response)
        return job_id, 200


@jobs_api.route("/jobs/<job_id>", methods=['PUT'])
def update_job(job_id):
    model = request.get_json().get('model', '')
    logs = request.get_json().get('logs', '')
    tb_logs = request.get_json().get('tb_logs', '')
    label_map = request.get_json().get('label_map', '')
    job_ref = db.reference('/jobs/'+job_id).update(
        {
            'model': model,
            'logs': logs,
            'tb_logs': tb_logs,
            'label_map': label_map
        }
    )
    # TODO: Run a script on an already running compute engine instance to create a dynamic endpoint for predictions.
    return "Success", 200
