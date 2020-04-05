from flask import Blueprint, request, jsonify
import time
import json
import logging
from firebase_admin import auth, db, exceptions, credentials
import paths.helpers

jobs_api = Blueprint("jobs_api", __name__)


@jobs_api.route("/jobs", methods=['POST'])
def create_job():
    job_type = request.get_json().get("type", "")
    dataset = request.get_json().get("dataset", "")
    created_by = request.get_json().get("created_by")
    created_at = request.get_json().get("created_at")

    user_ref = db.reference('/users/'+created_by).get()

    if created_by == "" or not user_ref.val():
        return "No such userid exists", 400
    
    if job_type == 'image_classification':
        


        pass



















        

    elif job_type == 'structured_classification':
        pass

    elif job_type == 'structured_prediction':
        pass

    elif job_type == 'custom':
        pass

    else:
        return "No such job type exists", 400