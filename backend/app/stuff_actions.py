from flask import Blueprint, request, jsonify, abort
from .assets.validate import valid_datas, stuff_exists, is_admin_in_session
from .models import Stuff
from . import db
stuff = Blueprint("stuff", __name__)

@stuff.route("/register", methods=["POST"])
def register_stuff():
    if request.method == "POST":
        try:
            if not is_admin_in_session():
                abort(401)
            stuff_data = request.get_json()
            if stuff_exists(stuff_data["name"],
                            stuff_data["position"]):
                return jsonify({
                    "status": 403,
                    "message": f"Stuff exists with this name - {stuff_data["name"], position - {stuff_data["position"]}}"
                }), 403
            
            # create stuff 
            new_stuff = Stuff()
            new_stuff.name = stuff_data["name"]
            new_stuff.picture_uri = stuff_data["picture_uri"] 
            new_stuff.position = stuff_data["position"]
            new_stuff.father_name = stuff_data["father_name"]
            new_stuff.address = stuff_data["address"]
            new_stuff.phone_no = stuff_data["phone_no"]
            new_stuff.email = stuff_data["email"]
            new_stuff.birth_date = stuff_data["birth_date"]
            
            #  add to session
            db.session.add(new_stuff)
            # commit to db
            db.session.commit()
            
            return jsonify({
                "status": 200,
                "message": "New Stuff Added"
            }), 200
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "Error while register new stuff",
                "error_msg": err
            }), 500

