from flask import Blueprint, request, url_for, render_template, jsonify, abort
from .assets.validate import is_admin_in_session, is_not_valid, guest_exists
from . import db
from werkzeug.security import generate_password_hash
from .models import Guest

guest = Blueprint("guest", __name__)

@guest.route("/register", methods=["POST"])
def register_guest():
    """
    allow_data_type: json
    methods: "POST"
    request_data: json_data ( name, picture_uri )
    summery: take guest register data (json) and add to guest table
    """
    if request.method == "POST":
        if not is_admin_in_session():
            abort(401)
        try:
            guest_data = request.get_json()
            if not is_not_valid(guest_data):
                return jsonify({
                    "status": 403,
                    "message": "Be sure your update datas all set"
                }), 403
            # generate token 
            initial_token = generate_password_hash(guest_data["name"])
            token = generate_password_hash(initial_token)
            if guest_exists(guest_data["name"],
                            token):
                return jsonify({
                    "status": 403,
                    "message": f"guest exists with this name - {guest_data["name"]}"
                }), 403
            
            # create guest 
            new_guest = Guest()
            new_guest.name = guest_data["name"]
            new_guest.picture_uri = guest_data["picture_uri"] 
            new_guest.token = token            
            new_guest.people_count = guest_data["people_count"]
            #  add to session
            db.session.add(new_guest)
            # commit to db
            db.session.commit()
            
            return jsonify({
                "status": 200,
                "message": "New guest Added"
            }), 200
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "Error while register new guest",
                "error_msg": err
            }), 500
            
@guest.route("/delete/<int:guest_id>", methods=["DELETE"])
def delete_guest(guest_id: int):
    """
    summery: will take guest_id as arg and delete if exists
    """
    if not is_admin_in_session():
        abort(401)
    try:
        guest = Guest.query.get(guest_id)
        if guest:
            db.session.delete(guest)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": f"guest {guest.name} deleted"
            })
        return jsonify({
            "status": 404,
            "message": f"guest with id: {guest_id} doesn't exists"
        }), 404
    except Exception as err:
        return jsonify({
            "status": 500,
            "message": "Error while deleting"
        })

@guest.route("/get_guest/<int:guest_id>")
def get_guest_info(guest_id: int):
    """
    summery: get guest all info by guest_id
    """
    if not is_admin_in_session():
        abort(401)
    try: 
        guest = Guest.query.get(guest_id)
        if guest:
            # format guest data as dict to return json
            guest_data = {
                "guest_id": guest.guest_id,
                "name": guest.name,
                "picture_uri": guest.picture_uri,
                "token": guest.token,
                "people_count": guest.people_count,
                "register_date": guest.register_date
            }
            return jsonify({
                "status": 200,
                "guest_info": guest_data
            }), 200
    except Exception as err:
        return jsonify({
            "status": 500,
            "message": "Error while looking for guest",
            "error_msg": err
        }), 500
    return jsonify({
        "status": 404,
        "message": f"guest ID: {guest_id} not found or exists"
    }), 404
    