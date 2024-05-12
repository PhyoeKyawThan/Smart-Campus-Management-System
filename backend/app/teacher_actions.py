from flask import Blueprint, jsonify, request, render_template, abort
from .models import Teacher
from . import db
from .assets.validate import is_admin_in_session, teacher_exists
teacher = Blueprint("teacher", __name__)


@teacher.route("/register", methods=["POST"])
def register_teacher():
    """
    allowed_data_type: json
    method: "POST"
    request_data: json_data ( name, picture_uri, department, position, nrc, father_name, address, phone_no, email )
    summery: take teacher data (json) and add register to teacher table  
    """
    if request.method == "POST":
        # check admin already exist or not
        if not is_admin_in_session():
            abort(401)
        # get teacher info
        teacher_data = request.get_json()
        try:
            if teacher_exists(teacher_data["name"],
                              teacher_data["department"],
                              teacher_data["position"]):
                return jsonify({
                    "status": 403,
                    "message": f"Teacher {teacher_data["name"]} exists"
                }), 403
            # if teacher doesn't exist 
            new_teacher = Teacher()
            new_teacher.name = teacher_data["name"]
            new_teacher.picture_uri = teacher_data["picture_uri"]
            new_teacher.department = teacher_data["department"]
            new_teacher.position = teacher_data["position"]
            new_teacher.nrc = teacher_data["nrc"]
            new_teacher.father_name = teacher_data["father_name"]
            new_teacher.address = teacher_data["address"]
            new_teacher.phone_no = teacher_data["phone_no"]
            new_teacher.email = teacher_data["email"]
            
            # add to db session
            db.session.add(new_teacher)
            # commit change 
            db.session.commit()
            return jsonify({
                "stauts": 200,
                "message": "New Teacher Added"
            }), 200
            
        except Exception as err:
            print(err)
            return jsonify({
                "status": 500,
                "message": "There is something wrong with the server."
            }), 500
            
@teacher.route("/delete/<int:teacher_id>", methods=["GET"])
def delete_teacher(teacher_id: int):
    """
    summery: will take student_id as arg and delete if exists
    """
    if not is_admin_in_session():
        abort(401)
    try:
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": f"Teacher {teacher.name} deleted"
            })
        return jsonify({
            "status": 404,
            "message": f"Teacher with id: {teacher_id} doesn't exists"
        }), 404
    except Exception as err:
        return jsonify({
            "status": 500,
            "message": "Error while deleting"
        })
