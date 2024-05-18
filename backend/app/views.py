from flask import Blueprint, render_template, abort
from . import db
from .assets.validate import is_admin_in_session

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    from .models import get_student_info, get_teacher_info
    return render_template("index.html", students=get_student_info(), teachers=get_teacher_info())

@views.route("/students")
def student_views():
    if not is_admin_in_session():
        return render_template("admin_login.html")
    from .models import get_student_info
    return render_template("student_view.html", students=get_student_info())

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")

@views.route("/protected")
def protected_route():
    from flask import session
    return session["current_admin"]

@views.route("/show")
def show():
    return render_template("send_mail.html")

@views.route("/send")
def send_mail_test():
    from .mail import send_mail
    is_send: tuple = send_mail({
        "subject": "Hello Dom",
        "recipients": ["@gmail.com"],
        "body": "Hello phyoe are u okey?"
    })
    print(is_send)
    if is_send[0]:
        return f"{is_send[1]}"
    return is_send[1]

@views.route("/register_teacher")
def teacher_register_view():
    return render_template("teacher/register.html")