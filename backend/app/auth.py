from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from .assets.validate import is_admin
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def admin_login():
    """
    summery: formdata as client request and key of admin are username, password
    """
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if is_admin(username, password):
            session["current_admin"] = {
                "username": username,
                "password": password
            }
            return redirect(url_for("views.home"))
        return redirect(url_for("views.admin_login_view", 
                                message="Incorrect Admin username or Password"))