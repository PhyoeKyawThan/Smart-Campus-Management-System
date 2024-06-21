from flask import Blueprint, render_template, abort, jsonify, request
from . import db
from .assets.validate import is_admin_in_session
from .viewModel import ViewModel

views = Blueprint("views", __name__)

# @views.route("/")
# def home():
#     if not is_admin_in_session():
#         return render_template("admin_login.html")
#     recent_pass = get_passes()
#     recent_pass.reverse()
#     return render_template("index.html",
#                            recent_pass=recent_pass[:10],
#                            students=get_student_info(), 
#                            teachers=get_teacher_info(), 
#                            campus_passes=get_passes(),
#                            staffs = get_staff_info())

@views.route("/get_info/<string:which>")
def get_info(which):
    from json import dumps
    view = ViewModel()
    return jsonify({
        "data": view.gate_passes(which)
    })

@views.route('/camera')
def camera():
    return render_template("camera.html")

@views.route("/students")
def student_views():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    from .models import get_student_info
    return render_template("student_view.html", students=get_student_info())

@views.route("/register_student")
def student_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("student/register.html")

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")

@views.route("/get_hash")
def get_hash():
    from .models import Student, Teacher, Staff
    from werkzeug.security import generate_password_hash
    import json
    # test_stu = Teacher.query.get(1)
    # test_tec = Teacher.query.get(1)
    people = Staff.query.get(1)
    # format_hash = {
    #                 "student_id": test_stu.student_id,
    #                 "name": test_stu.name,
    #                 "roll_no": test_stu.roll_no,
    #                 "father_name": test_stu.father_name,
    #                 "current_semester": test_stu.current_semester
    #             }
    # format_hash = {
    #                 "teacher_id": test_tec.teacher_id,
    #                 "name": test_tec.name,
    #                 "department": test_tec.department,
    #                 "position": test_tec.position,
    #                 "nrc": test_tec.nrc,
    #                 "birth_date": str(test_tec.birth_date)
    #             }
    format_hash = {
                    "staff_id": people.staff_id,
                    "name": people.name,
                    "position": people.position,
                    "birth_date": str(people.birth_date)
                }
    token = {
        "id": people.staff_id,
        "who": "staff",
        "token": generate_password_hash(json.dumps(format_hash))
    }
    return jsonify(token)

@views.route("/times")
def times():
    from .models import get_passes
    return jsonify({
        "data": get_passes()
    })

# @views.route("/search_by_date", methods=["POST"])
# def search_by_date():
#     try:
#         search_date = request.get_json()
#         for pass_ in get_passes():
#             print(pass_)
#         return jsonify({
#             "success": True,
#             "data": [pass_ for pass_ in get_passes() if str(pass_["date"]) == search_date["date"]]
#         })
#     except Exception as err:
#         print(err)