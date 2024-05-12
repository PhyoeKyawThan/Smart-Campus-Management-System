from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from .assets.validate import check_admin_in_session, is_admin
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def admin_login():
    """
    summery: formdata as client request and key of admin are username, password
    """
    if request.method == 'POST':
        check_admin_in_session()
        username = request.form["username"]
        password = request.form["password"]
        if is_admin(username, password):
            session["current_admin"] = {
                "username": username,
                "password": password
            }
            return render_template("index.html")
        return redirect(url_for("views.admin_login_view", 
                                message="Incorrect Admin username or Password"))