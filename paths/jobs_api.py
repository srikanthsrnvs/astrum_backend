from flask import Blueprint, request, jsonify
import time
import json
import logging
from firebase_admin import auth, db, exceptions, credentials
import paths.helpers

jobs_api = Blueprint("jobs_api", __name__)


@jobs_api.route("/jobs", methods=['POST'])
def create_job():
    pass

@jobs_api.route("/jobs/<jobid>", methods=['GET'])
def get_job(jobid):
    pass