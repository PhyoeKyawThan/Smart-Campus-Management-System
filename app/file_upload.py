from flask import Blueprint, request, url_for, current_app, jsonify, abort
from .assets.validate import is_admin_in_session
from werkzeug.utils import secure_filename
from os import path, remove, makedirs

file =  Blueprint('file',__name__)

@file.route("/upload/<string:is_who>", methods=['POST'])
def file_upload(is_who):
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

            # Ensure the directory for the specified category exists
            if is_who not in ['student', 'teacher', 'guest', 'staff']:
                return jsonify({
                    "status": "fail",
                    "message": "Invalid category"
                }), 400

            category_dir = path.join(current_app.config["PROFILE_DIR"], is_who)
            if not path.exists(category_dir):
                makedirs(category_dir)

            image_path = path.join(category_dir, image_name)
            if path.exists(image_path):
                return jsonify({
                    "status": "fail",
                    "message": "Already uploaded this file",
                    "image_uri": f"static/profiles/{is_who}/{image_name}"
                }), 200

            try:
                image.save(image_path)
                return jsonify({
                    "status": "Success",
                    "message": "Image Uploaded",
                    "image_uri": f"static/profiles/{is_who}/{image_name}"
                }), 200
            except FileNotFoundError as err:
                return jsonify({
                    "status": "Fail",
                    "message": "Error while Uploading to Server",
                    "error_msg": err.strerror
                }), 500

        return jsonify({
            "status": 403,
            "message": "It seems like you haven't selected any image"
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