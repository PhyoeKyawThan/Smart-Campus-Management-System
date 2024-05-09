from flask import Blueprint, request, session, render_template, redirect, jsonify
from .models import Student
from . import db
from .validate import student_exists
register = Blueprint("register", __name__)

@register.route("/register", methods=["GET", "POST"])
def register_student():
    """
    allow_data_type: json
    methods: "POST"
    parems: json_data ( name, picture_uri, roll_no, current_semester, nrc, father, address, phone_no, email )
    summery: take student register data (json) and add to Student table
    """
    if request.method == "POST":
        student_data = request.get_json()
        try:
            if student_exists(student_data["name"],
                              student_data["roll_no"]):
                return jsonify({
                    "status": 403,
                    "message": f"Student exists with name - {student_data["name"]} and roll_no - {student_data["roll_no"]}"

                })
            # create student object with new data 
            new_student = Student(
            student_data["name"],
            student_data["picture_uri"],
            student_data["roll_no"],
            student_data["current_semester"],
            student_data["nrc"],
            student_data["father"],
            student_data["address"],
            student_data["phone_no"],
            student_data["email"]
        )
            db.session.add(new_student)
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
    return render_template("errors/method_not_allowed.html")