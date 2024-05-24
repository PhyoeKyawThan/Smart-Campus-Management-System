from flask import Blueprint, render_template, abort
from . import db
from .assets.validate import is_admin_in_session

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    from .models import get_student_info, get_teacher_info, get_trackpass
    return render_template("index.html",
                           recent_pass=get_trackpass()[:5],
                           students=get_student_info(), 
                           teachers=get_teacher_info(), 
                           campus_passes=get_trackpass())

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
    from flask import request
    from werkzeug.security import generate_password_hash
    student_id = request.args.get("id")
    from .models import Teacher, Staff
    from flask import jsonify
    student = db.session.query(Staff).get(student_id).track_passes
    for track in student:
        print("Pass ID - ", track.pass_id)
        for time in track.times:
            if time.in_time:
                print(f"In - {time.in_time}")
            if time.out_time:
                print(f"Out - {time.out_time}")
    return ""