from flask import Blueprint, render_template, abort
from . import db
from .assets.validate import check_admin_in_session

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if not check_admin_in_session():
        return render_template("admin_login.html")
    return render_template("base.html")

@views.route("/students")
def student_views():
    from .models import get_student_info
    return render_template("student_view.html", students=get_student_info())

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")
