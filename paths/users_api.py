import json
import logging
import time

from firebase_admin import auth, db, exceptions
from flask import Blueprint, jsonify, request

users_api = Blueprint("users_api", __name__)


@users_api.route('/users', methods=['POST'])
def sign_up():
    email = request.get_json().get('email', '')
    password = request.get_json().get('password', '')
    display_name = request.get_json().get('display_name', '')

    try:
        user = auth.create_user(
            display_name=display_name,
            email=email,
            password=password
        )
    except exceptions.FirebaseError as ex:
        logging.warning("Error: {}, Data: {}".format(ex, request.get_json()))
        message = str(ex)
        return jsonify({"error": message}), 400

    logging.info("Created a new user with id: {}".format(user.uid))

    try:
        db.reference('users').set(
            {
                user.uid: {
                    "email": user.email,
                    "display_name": user.display_name,
                    "created_at": int(time.time())
                }
            }
        )
    except exceptions.FirebaseError as ex:
        delete_user(user.uid)
        logging.warning("Error: {}, Data: {}".format(ex, request.get_json()))
        message = str(ex)
        return jsonify({"error": message}), 400

    return jsonify({"success": "User created"}), 200


@users_api.route('/users/<userid>', methods=['GET'])
def get_user_details(userid):

    try:
        user_data = db.reference('users/{}'.format(userid)).get()
    except exceptions.FirebaseError as ex:
        logging.warning("Error: {}, Data: {}".format(ex, request.get_json()))
        message = str(ex)
        return jsonify({"error": message}), 400

    logging.info("Returned user data for user {}".format(userid))

    return jsonify(user_data), 200


def delete_user(uid):

    try:
        auth.delete_user(uid)
    except exceptions.FirebaseError as ex:
        logging.warning("Error: {}, Data: {}".format(ex, uid))
        return False

    return True
