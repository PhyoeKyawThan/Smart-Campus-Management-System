from flask import Blueprint, request, url_for, current_app, jsonify, abort
from .assets.validate import is_admin_in_session
from werkzeug.utils import secure_filename
from os import path, remove

file =  Blueprint('file',__name__)

@file.route("/upload", methods=['POST'])
def file_upload():
    """
    request_type: multi/form-data
    key(name): "image"
    return: json
    summery: take form-data and save to static/profiles and return appropriate json 
    """
    if not is_admin_in_session():
        abort(401)
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files["image"]
            image_name = secure_filename(image.filename)
            image_path = path.join(current_app.config["PROFILE_DIR"], image_name)
            if path.exists(image_path):
                return jsonify({
                    "status": "fail",
                    "message": "Already uploaded this file",
                    "image_uri": "static/profiles" + image_name
                }), 200
            try:
                image.save(path.join(current_app.config["PROFILE_DIR"], image_name))
                return jsonify({
                    "status": "Success",
                    "message": "Image Uploaded",
                    "image_uri": "static/profiles/" + image_name
                })
                # pass
            except FileNotFoundError as err:
                return jsonify({
                    "status": "Fail",
                    "message": "Error while Uploading to Server",
                    "error_msg": err.strerror
                }), 500
        
        return jsonify({
            "status": 403,
            "message": "Seen like u haven't selected any image"
        }), 403

@file.route("/delete/<string:image_name>", methods=["DELETE"])
def delete_image(image_name: str):
    if not is_admin_in_session():
        abort(401)
    if image_name:
        try:
            remove(path=path.join(current_app.config["PROFILE_DIR"], image_name))
            return jsonify({
                "status": "success",
                "message": f"Deleted {image_name}"
            }), 200
        except FileNotFoundError as err:
            return jsonify({
                    "status": "Fail",
                    "message": "Already Deleted or File Not Found in target will deleted image",
                    "error_msg": err.strerror
                }), 500