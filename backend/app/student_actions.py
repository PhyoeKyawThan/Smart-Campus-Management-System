from flask import Blueprint, request, render_template, redirect, jsonify, abort
from .models import Student
from . import db
from .assets.validate import student_exists, is_admin_in_session, valid_datas
student = Blueprint("student", __name__)

@student.route("/register", methods=["POST"])
def register_student():
    """
    allow_data_type: json
    methods: "POST"
    request_data: json_data ( name, picture_uri, roll_no, current_semester, nrc, father, address, phone_no, email )
    summery: take student register data (json) and add to Student table
    """
    if request.method == "POST":
        # check admin have already logged in or not 
        if not is_admin_in_session():
            abort(401)
        student_data = request.get_json()
        try:
            if student_exists(student_data["roll_no"]):
                return jsonify({
                    "status": 403,
                    "message": f"Student exists with roll_no - {student_data["roll_no"]}",
                }), 403
            # create student object
            new_student = Student()
            # add incoming data to respective field
            new_student.name = student_data["name"]
            new_student.picture_uri = student_data["picture_uri"]
            new_student.roll_no = student_data["roll_no"]
            new_student.current_semester = student_data["current_semester"]
            new_student.nrc = student_data["nrc"]
            new_student.father_name = student_data["father_name"]
            new_student.address = student_data["address"]
            new_student.phone_no = student_data["phone_no"]
            new_student.email = student_data["email"]

            db.session.add(new_student)
            # commit to database
            db.session.commit()
            
            return jsonify({
                'status': 200,
                'message': "New Student Added"
            }), 200
        except Exception as err:
            print(err)
            return jsonify({
                "status": 500, 
                "message": "Error while inserting to database"
            }), 500

@student.route("/edit_student/<int:student_id>", methods=["POST"])
def edit_student_info(student_id: int):
    """
    request_data: json 
                    keys - name
                           picture_uri
                           roll_no
                           current_semester
                           nrc
                           father_name
                           address
                           phone_no
                           email
    method: "POST"
    summery: request json data 
    - update student table with getting specified Student object by student_id, 
    """
    if request.method == "POST":
        if not is_admin_in_session():
            abort(401)
        edit_data = request.get_json()
        if not valid_datas(edit_data):
            return jsonify({
                "status": 403,
                "message": "Be sure your update datas all set"
            }), 403
        try:
            edit_student = Student.query.get(student_id)
            if edit_student:
                edit_student.name = edit_data["name"]
                edit_student.picture_uri = edit_data["picture_uri"]
                edit_student.roll_no = edit_data["roll_no"]
                edit_student.current_semester = edit_data["current_semester"]
                edit_student.nrc = edit_data["nrc"]
                edit_student.father_name = edit_data["father_name"]
                edit_student.address = edit_data["address"]
                edit_student.phone_no = edit_data["phone_no"]
                edit_student.email = edit_data["email"]
                
                # final commit to db
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"Student {edit_student.name}'s info updated"
                }), 200
        except Exception as err:
            print(err)
            return jsonify({
                "status": 500,
                "message": "There's problem while updating student datas"
            }), 500
    

@student.route("/get_student/<int:student_id>")
def get_student_info(student_id: int):
    """
    summery: get student all info by student_id
    """
    if not is_admin_in_session():
        abort(401)
    try: 
        student = Student.query.get(student_id)
        if student:
            # format student data as dict to return json
            student_data = {
                "student_id": student.student_id,
                "name": student.name,
                "picture_uri": student.picture_uri,
                "roll_no": student.roll_no,
                "current_semester": student.current_semester,
                "nrc": student.nrc,
                "father_name": student.father_name,
                "address": student.address,
                "phone_no": student.phone_no,
                "email": student.email,
                "register_date": student.register_date
            }
            return jsonify({
                "status": 200,
                "student_info": student_data
            }), 200
    except Exception as err:
        print(err)
        return jsonify({
            "status": 500,
            "message": "Error while looking for student"
        })
    return jsonify({
        "status": 404,
        "message": f"Student ID: {student_id} not found or exists"
    }), 404
    


@student.route("/delete/<int:student_id>", methods=["GET"])
def delete_student(student_id):
    """
    summery: will take student_id as arg and delete if exists
    """
    if request.method == 'GET':
        if not is_admin_in_session():
            abort(401)
        try:
            student = Student.query.get(student_id)
            if student:
                db.session.delete(student)
                db.session.commit()
                
                return jsonify({
                    "status": 200,
                    "message": f"Successfully deleted <name - {student.name}>"
                }), 200
            return jsonify({
                "status": 404,
                "message": f"Student ID {student_id} doesn't exists"
            }), 404
        except Exception as err:
            print(err)
            return jsonify({
                "status": 500,
                "message": "Something wrong with server"
            }), 500