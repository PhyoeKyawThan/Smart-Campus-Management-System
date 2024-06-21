from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from .assets.validate import is_admin
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def admin_login():
    """
    summery: formdata as client request and key of admin are username, password
    """
    if request.method == 'POST':
        try:
            username = request.form["username"]
            password = request.form["password"]
        except KeyError as err:
            return redirect(url_for("views.admin_login_view", 
                             message="Be sure your requested login datas is correct"))
        if is_admin(username, password):
            session["current_admin"] = {
                "username": username,
                "password": password
            }
            return redirect(url_for("views.home"))
        return redirect(url_for("views.admin_login_view", 
                                message="Incorrect Admin username or Password"))
        
@auth.route("/logout")
def logout_admin():
    session.clear()
    return redirect(url_for("views.admin_login_view"))