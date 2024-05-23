from flask import Blueprint, request, jsonify, abort
from ..assets.validate import is_admin_in_session
from .track_pass_control import add_trackpass
from werkzeug.security import generate_password_hash
import json
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
        add_trackpass(data)
        
            # return student.name
    return generate_password_hash(json.dumps({
                    "student_id": 1,
                    "name": "Alice Johnson",
                    "roll_no": "A12345",
                    "father_name": "John Johnson",
                    "current_semester": 4
                }))