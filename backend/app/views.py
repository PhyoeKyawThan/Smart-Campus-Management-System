from flask import Blueprint, render_template, abort, jsonify, request
from . import db
from .assets.validate import is_admin_in_session
from .models import get_student_info, get_teacher_info, get_trackpass

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    recent_pass = get_trackpass()
    recent_pass.reverse()
    return render_template("index.html",
                           recent_pass=recent_pass[:10],
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
    # from flask import request
    # from werkzeug.security import generate_password_hash
    # student_id = request.args.get("id")
    # from .models import Teacher, Staff
    # student = db.session.query(Staff).get(student_id).track_passes
    from .models import get_trackpass
    return jsonify({
        "data": get_trackpass()
    })

@views.route("/search_by_date", methods=["POST"])
def search_by_date():
    try:
        search_date = request.get_json()
        for pass_ in get_trackpass():
            print(pass_)
        return jsonify({
            "success": True,
            "data": [pass_ for pass_ in get_trackpass() if str(pass_["date"]) == search_date["date"]]
        })
    except Exception as err:
        print(err)