from flask import Blueprint, render_template
from . import db
from .models import Student

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("base.html")

@views.route("/admin_login")
def admin_login_view():
    return render_template("admin_login.html")