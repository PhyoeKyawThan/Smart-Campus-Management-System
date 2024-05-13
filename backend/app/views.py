from flask import Blueprint, render_template, abort
from . import db
from .assets.validate import is_admin_in_session

views = Blueprint("views", __name__)

@views.route("/")
def home():
    # if not is_admin_in_session():
    #     return render_template("admin_login.html")
    from .models import get_student_info, get_teacher_info
    return render_template("index.html", students=get_student_info(), teachers=get_teacher_info())

@views.route("/students")
def student_views():
    from .models import get_student_info
    return render_template("student_view.html", students=get_student_info())

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")
