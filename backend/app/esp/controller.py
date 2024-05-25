from flask import Blueprint, request, jsonify, abort
from ..assets.validate import is_admin_in_session
from werkzeug.security import generate_password_hash
import json
from .track import Track
controller = Blueprint("controller", __name__)


@controller.route("/who_pass", methods=["POST", "GET"])
def who_pass():
    """
    format_data = {
                    "student_id": student.student_id,
                    "name": student.name,
                    "roll_no": student.roll_no,
                    "father_name": student.father_name,
                    "current_semester": student.current_semester
                }
    summery: 
    """
    if not is_admin_in_session():
        abort(401)
    if request.method == "POST":
        data = request.get_json()
        new_track = Track(data["who"])
        new_track.add_pass(datas=data)
        
            # return student.name
    return f"passed - {data["id"]}"