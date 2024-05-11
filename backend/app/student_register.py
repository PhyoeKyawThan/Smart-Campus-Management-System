from flask import Blueprint, request, render_template, redirect, jsonify, abort
from .models import Student
from . import db
from datetime import datetime
from .validate import student_exists, check_admin_in_session
register = Blueprint("register", __name__)

@register.route("/register", methods=["POST"])
def register_student():
    """
    allow_data_type: json
    methods: "POST"
    parems: json_data ( name, picture_uri, roll_no, current_semester, nrc, father, address, phone_no, email )
    summery: take student register data (json) and add to Student table
    """
    if request.method == "POST":
        # check admin have already logged in or not 
        if not check_admin_in_session():
            abort(401)
        student_data = request.get_json()
        try:
            if student_exists(student_data["roll_no"]):
                return jsonify({
                    "status": 403,
                    "message": f"Student exists with roll_no - {student_data["roll_no"]}",
                })
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
            db.session.close()
            return jsonify({
                'status': 200,
                'message': "New Student Added"
            })
        except Exception as err:
            print(err)
            return jsonify({
                "status": 500, 
                "message": "Error while inserting to database"
            })