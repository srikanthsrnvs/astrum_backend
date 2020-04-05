import base64
import json
import logging

from flask import Flask, jsonify, request, blueprints
from flask_cors import CORS
from six.moves import http_client
from firebase_admin import *
from paths.users_api import users_api
from paths.jobs_api import jobs_api
from paths.datasets_api import datasets_api
import firebase_admin

cred = credentials.Certificate("./astrumdashboard-firebase-adminsdk-a9922-baf7120ba2.json")

firebase = firebase_admin.initialize_app(cred, {
    "databaseURL": "https://astrumdashboard.firebaseio.com/"
})
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(users_api)
app.register_blueprint(datasets_api)
app.register_blueprint(jobs_api)


@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.exception('An error occured while processing the request.')
    response = jsonify({
        'code': http_client.INTERNAL_SERVER_ERROR,
        'message': 'Exception: {}'.format(e)})
    response.status_code = http_client.INTERNAL_SERVER_ERROR
    return response


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
