from flask import Blueprint, render_template, jsonify

errors = Blueprint("erorrs", __name__)

@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/page_not_found.html"), 404

@errors.app_errorhandler(405)
def page_not_found(e):
    return render_template("errors/method_not_allowed.html"), 405

@errors.app_errorhandler(401)
def page_not_found(e):
    return render_template("errors/unauthorized.html"), 401

@errors.app_errorhandler(415)
def page_not_found(e):
    return jsonify({
        "status": 415,
        "message" : "Unsupported Media Type"
    }), 415