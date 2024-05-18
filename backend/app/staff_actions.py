from flask import Blueprint, request, jsonify, abort
from .assets.validate import is_not_valid, staff_exists, is_admin_in_session
from .models import Staff
from . import db
staff = Blueprint("staff", __name__)

@staff.route("/register", methods=["POST"])
def register_staff():
    """
    allow_data_type: json
    methods: "POST"
    request_data: json_data ( name, picture_uri, position, father_name,
    address, phone_no, email, birth_date)
    summery: take staff register data (json) and add to staff table
    """
    if request.method == "POST":
        if not is_admin_in_session():
            abort(401)
        try:
            staff_data = request.get_json()
            if not is_not_valid(staff_data):
                return jsonify({
                    "status": 403,
                    "message": "Be sure your update datas all set"
                }), 403
            if staff_exists(staff_data["name"],
                            staff_data["position"]):
                return jsonify({
                    "status": 403,
                    "message": f"staff exists with this name - {staff_data["name"], position - {staff_data["position"]}}"
                }), 403
            
            # create staff 
            new_staff = staff()
            new_staff.name = staff_data["name"]
            new_staff.picture_uri = staff_data["picture_uri"] 
            new_staff.position = staff_data["position"]
            new_staff.father_name = staff_data["father_name"]
            new_staff.address = staff_data["address"]
            new_staff.nrc = staff_data["nrc"]
            new_staff.phone_no = staff_data["phone_no"]
            new_staff.email = staff_data["email"]
            new_staff.birth_date = staff_data["birth_date"]
            
            #  add to session
            db.session.add(new_staff)
            # commit to db
            db.session.commit()
            
            return jsonify({
                "status": 200,
                "message": "New staff Added"
            }), 200
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "Error while register new staff",
                "error_msg": err
            }), 500

@staff.route("/edit_staff/<int:staff_id>", methods=["POST"])
def edit_staff_info(staff_id: int):
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
    - update staff table with getting specified staff object by staff_id, 
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
            edit_staff = Staff.query.get(staff_id)
            if edit_staff:
                edit_staff.name = edit_data["name"]
                edit_staff.picture_uri = edit_data["picture_uri"] 
                edit_staff.position = edit_data["position"]
                edit_staff.father_name = edit_data["father_name"]
                edit_staff.address = edit_data["address"]
                edit_staff.nrc = edit_data["nrc"]
                edit_staff.phone_no = edit_data["phone_no"]
                edit_staff.email = edit_data["email"]
                edit_staff.birth_date = edit_data["birth_date"]
                
                # commit change 
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"staff {edit_staff.staff_id}'s info Updated"
                }), 200
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "There's problem while updating staff datas",
                "error_msg": err
            }), 500


@staff.route("/get_staff/<int:staff_id>")
def get_staff_info(staff_id: int):
    """
    summery: get staff all info by staff_id
    """
    if not is_admin_in_session():
        abort(401)
    try: 
        staff = Staff.query.get(staff_id)
        if staff:
            # format staff data as dict to return json
            staff_data = {
                "staff_id": staff.staff_id,
                "name": staff.name,
                "picture_uri": staff.picture_uri,
                "position": staff.position,
                "nrc": staff.nrc,
                "father_name": staff.father_name,
                "address": staff.address,
                "phone_no": staff.phone_no,
                "email": staff.email,
                "birth_date": staff.birth_date,
                "register_date": staff.register_date
            }
            return jsonify({
                "status": 200,
                "staff_info": staff_data
            }), 200
    except Exception as err:
        return jsonify({
            "status": 500,
            "message": "Error while looking for staff",
            "error_msg": err
        }), 500
    return jsonify({
        "status": 404,
        "message": f"staff ID: {staff_id} not found or exists"
    }), 404
    

@staff.route("/delete/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id: int):
    """
    summery: will take staff_id as arg and delete if exists
    """
    if request.method == 'DELETE':
        if not is_admin_in_session():
            abort(401)
        try:
            staff = Staff.query.get(staff_id)
            if staff:
                db.session.delete(staff)
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"Successfully deleted <name - {staff.name}>"
                }), 200
            return jsonify({
                "status": 404,
                "message": f"staff ID {staff_id} doesn't exists"
            }), 404
        except Exception as err:
            return jsonify({
                "status": 500,
                "message": "Something wrong with server",
                "error_msg": err
            }), 500