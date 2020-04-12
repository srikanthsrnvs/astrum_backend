import json
import logging
import time
from uuid import uuid4

import requests
from firebase_admin import auth, credentials, db, exceptions
from flask import Blueprint, jsonify, request
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

from paths.helpers import create_http_body, create_startup_script, url

jobs_api = Blueprint("jobs_api", __name__)


@jobs_api.route("/jobs", methods=['POST'])
def create_job():
    job_type = request.get_json().get("type", "")
    dataset = request.get_json().get("dataset", "")
    created_by = request.get_json().get("created_by")
    created_at = request.get_json().get("created_at")
    job_name = request.get_json().get('name', "")

    user_ref = db.reference('/users/'+created_by).get()

    if created_by == "" or not user_ref:
        return "No such userid exists", 400

    if job_type == 'image_classification' or job_type == 'object_detection' or job_type == 'object_localization':
        job_id = str(uuid4()).lower()
        
        # Create a reference for the job in the database
        db.reference('/jobs/'+job_id).set({
            'created_by': created_by,
            'created_at': created_at,
            'type': job_type,
            'dataset': dataset,
            'name': job_name,
            'status': 0
        })

        # Append the job to the current queue putting it last
        job_queue_ref = db.reference('/job_queue')
        job_queue = job_queue_ref.get() if job_queue_ref.get() else []
        job_queue.append(job_id)
        job_queue_ref.set(job_queue)

        # Append the job to the jobs the user has created before
        user_job_ref = db.reference('/users/{}/jobs'.format(created_by))
        jobs = user_job_ref.get() if user_job_ref.get() else []
        jobs.append(job_id)
        user_job_ref.set(jobs)
        return jsonify({'job_id': job_id, 'status': 'success'}), 200



@jobs_api.route("/jobs/<job_id>", methods=['PUT'])
def update_job(job_id):
    status = request.get_json().get('status', "")
    
    # Means that training on compute engine is complete
    if status == 2:
        model = request.get_json().get('model', '')
        logs = request.get_json().get('logs', '')
        tb_logs = request.get_json().get('tb_logs', '')
        label_map = request.get_json().get('label_map', '')
        serving_model = request.get_json().get('serving_model', '')
        job_ref = db.reference('/jobs/'+job_id).update(
            {   
                'serving_model': serving_model,
                'model': model,
                'logs': logs,
                'tb_logs': tb_logs,
                'label_map': label_map,
                'status': status,
                'finished_training_at': int(time.time())
            }
        )

        return jsonify({'status': 'success'}), 200

    # Means that building the prediction endpoint on compute engine is complete
    if status == 3:
        pass
