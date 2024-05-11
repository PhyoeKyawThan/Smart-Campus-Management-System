from flask import Blueprint, render_template, abort
from . import db
from .validate import check_admin_in_session

views = Blueprint("views", __name__)

@views.route("/")
def home():
    if not check_admin_in_session():
        return render_template("admin_login.html")
    return render_template("base.html")

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")