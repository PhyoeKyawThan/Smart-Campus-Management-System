from flask import Blueprint, request, jsonify, abort
from .assets.validate import is_not_valid, stuff_exists, is_admin_in_session
from .models import Stuff
from . import db
stuff = Blueprint("stuff", __name__)

@stuff.route("/register", methods=["POST"])
def register_stuff():
    """
    allow_data_type: json
    methods: "POST"
    request_data: json_data ( name, picture_uri, position, father_name,
    address, phone_no, email, birth_date)
    summery: take stuff register data (json) and add to Stuff table
    """
    if request.method == "POST":
        if not is_admin_in_session():
            abort(401)
        try:
            stuff_data = request.get_json()
            if not is_not_valid(stuff_data):
                return jsonify({
                    "status": 403,
                    "message": "Be sure your update datas all set"
                }), 403
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
            new_stuff.nrc = stuff_data["nrc"]
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

@stuff.route("/edit_stuff/<int:stuff_id>", methods=["POST"])
def edit_stuff_info(stuff_id: int):
    """
    request_data: json 
                    keys - name
                           picture_uri
                           position
                           father_name
                           address
                           phone_no
                           email
                           birth_date
    method: "POST"
    summery: request json data 
    - update stuff table with getting specified Stuff object by stuff_id, 
    """
    if request.method == "POST":
        if not is_admin_in_session():
            abort(401)
        edit_data = request.get_json()
        if not is_not_valid(edit_data):
            return jsonify({
                "status": 403,
                "message": "Be sure ur updates all set"
            })
        try:
            edit_stuff = Stuff.query.get(stuff_id)
            if edit_stuff:
                edit_stuff.name = edit_data["name"]
                edit_stuff.picture_uri = edit_data["picture_uri"] 
                edit_stuff.position = edit_data["position"]
                edit_stuff.father_name = edit_data["father_name"]
                edit_stuff.address = edit_data["address"]
                edit_stuff.nrc = edit_data["nrc"]
                edit_stuff.phone_no = edit_data["phone_no"]
                edit_stuff.email = edit_data["email"]
                edit_stuff.birth_date = edit_data["birth_date"]
                
                # commit change 
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"Stuff {edit_stuff.stuff_id}'s info Updated"
                }), 200
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "There's problem while updating stuff datas",
                "error_msg": err
            }), 500


@stuff.route("/get_stuff/<int:stuff_id>")
def get_stuff_info(stuff_id: int):
    """
    summery: get stuff all info by stuff_id
    """
    if not is_admin_in_session():
        abort(401)
    try: 
        stuff = Stuff.query.get(stuff_id)
        if stuff:
            # format stuff data as dict to return json
            stuff_data = {
                "stuff_id": stuff.stuff_id,
                "name": stuff.name,
                "picture_uri": stuff.picture_uri,
                "position": stuff.position,
                "nrc": stuff.nrc,
                "father_name": stuff.father_name,
                "address": stuff.address,
                "phone_no": stuff.phone_no,
                "email": stuff.email,
                "birth_date": stuff.birth_date,
                "register_date": stuff.register_date
            }
            return jsonify({
                "status": 200,
                "stuff_info": stuff_data
            }), 200
    except Exception as err:
        return jsonify({
            "status": 500,
            "message": "Error while looking for stuff",
            "error_msg": err
        }), 500
    return jsonify({
        "status": 404,
        "message": f"stuff ID: {stuff_id} not found or exists"
    }), 404
    

@stuff.route("/delete/<int:stuff_id>", methods=["DELETE"])
def delete_stuff(stuff_id: int):
    """
    summery: will take stuff_id as arg and delete if exists
    """
    if request.method == 'DELETE':
        if not is_admin_in_session():
            abort(401)
        try:
            stuff = Stuff.query.get(stuff_id)
            if stuff:
                db.session.delete(stuff)
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"Successfully deleted <name - {stuff.name}>"
                }), 200
            return jsonify({
                "status": 404,
                "message": f"stuff ID {stuff_id} doesn't exists"
            }), 404
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "Something wrong with server",
                "error_msg": err
            }), 500