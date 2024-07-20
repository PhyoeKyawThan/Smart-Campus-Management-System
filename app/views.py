from flask import Blueprint, render_template, abort, jsonify, request, Response
from . import db
from .assets.validate import is_admin_in_session
from .viewModel import ViewModel
# from . import socket as socketio
from .event_ import generate

views = Blueprint("views", __name__)

# @views.route("/test")
# def test_event():
#     return render_template("test.html")

# @views.route('/stream_passes/<string:who>')
# def stream(who):
    # from flask import current_app
    # return Response(generate(current_app, who), mimetype='text/event-stream')

@views.route("/")
def home():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    return render_template("index.html",
                           students=view.get_student_info(),
                           teachers=view.get_teacher_info()) 

@views.route("/page/<string:page>")
def get_page(page: str):
    return render_template(f"{page}/index.html")


@views.route("/get_info/<string:which>")
def get_info(which):
    view = ViewModel()
    return jsonify({
        "data": view.gate_passes(which)
    })

@views.route('/camera')
def camera():
    return render_template("camera.html")

@views.route("/get_all_students/<int:limit>/<int:offset>")
def student_views(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    students = view.get_student_info(limit, offset)
    return jsonify(students)

@views.route("/search_student/<string:roll_no>")
def get_student_id(roll_no):
    view = ViewModel()
    student = view.search_student_by_roll(roll_no)
    return jsonify(student)

@views.route("/register_student")
def student_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("student/register.html")
# student
@views.route("/get_all_teachers/<int:limit>/<int:offset>")
def get_all_teachers(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    teachers = view.get_teacher_info(limit, offset)
    return jsonify(teachers)

@views.route("/search_teacher/<string:name>")
def search_teacher(name):
    view = ViewModel()
    teacher = view.search_teacher_by_name(name)
    return jsonify(teacher)

@views.route("/register_teacher")
def teacher_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("teacher/register.html")
# teacher



@views.route("/register_staff")
def staff_register_view():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    return render_template("staff/register.html")

@views.route("/get_all_staff/<int:limit>/<int:offset>")
def get_all_staff(limit: int, offset: int):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    staff = view.get_staff_info(limit=limit ,offset=offset)
    return jsonify(staff)

@views.route("/search_staff/<string:name>")
def search_staff(name):
    view = ViewModel()
    teacher = view.search_staff_by_name(name)
    return jsonify(teacher)
#staff
@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")

@views.route("/get_passes/<string:which_>")
def get_passes(which_):
    if not is_admin_in_session():
        return render_template("admin_login.html")
    view = ViewModel()
    passes = view.gate_passes(which_)
    return jsonify(passes)

@views.route("/get_hash")
def get_hash():
    from .models import Student, Teacher, Staff
    from werkzeug.security import generate_password_hash
    import json
    test_stu = Student.query.get(5)
    # test_tec = Teacher.query.get(1)
    # people = Staff.query.get(6)
    format_hash = {
                    "student_id": test_stu.student_id,
                    "name": test_stu.name,
                    "roll_no": test_stu.roll_no,
                    "father_name": test_stu.father_name,
                    "current_semester": test_stu.current_semester,
                    "roll_no": test_stu.roll_no,
                    "father_name": test_stu.father_name,
                    "current_semester": test_stu.current_semester
                }
    # format_hash = {
    #                 "teacher_id": test_tec.teacher_id,
    #                 "name": test_tec.name,
    #                 "department": test_tec.department,
    #                 "position": test_tec.position,
    #                 "nrc": test_tec.nrc,
    #                 "birth_date": str(test_tec.birth_date)
    #             }#                 "roll_no": test_stu.roll_no,
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
    #             }    #                 "roll_no": test_stu.roll_no,
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
    #             }}
    # format_hash = {
    #                 "teacher_id": test_tec.teacher_id,
    #                 "name": test_tec.name,
    #                 "department": test_tec.department,
    #                 "position": test_tec.position,
    #                 "nrc": test_tec.nrc,
    #                 "birth_date": str(test_tec.birth_date)
    #             }
    # format_hash = {
    #                 "staff_id": people.staff_id,
    #                 "name": people.name,
    #                 "position": people.position,
    #                 "birth_date": str(people.birth_date)
    #             }
    token = {
        "id": test_stu.student_id,
        "who": "student",
        "token": generate_password_hash(json.dumps(format_hash))
    }
    return jsonify(token)

@views.route("/times")
def times():
    from .models import get_passes
    return jsonify({
        "data": get_passes()
    })
