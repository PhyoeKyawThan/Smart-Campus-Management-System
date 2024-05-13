from flask import Blueprint, request

stuff = Blueprint("stuff", __name__)

@stuff.route("/register", methods=["POST"])
def register_stuff():
    if request.method == "POST":
        stuff_data = request.get_json()
        