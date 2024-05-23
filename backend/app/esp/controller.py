from flask import Blueprint, request, jsonify, abort
from ..assets.validate import is_admin_in_session
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Student, TrackPass
import json
controller = Blueprint("controller", __name__)

# def add_trackpass(roll: str, dat): bool:
#     match(roll):
#         case "student":
#             new_student = Student()

@controller.route("/who_pass", methods=["POST"])
def who_pass():
    """
    summery: 
    """
    if not is_admin_in_session():
        abort(401)
    if request.method == "POST":
        data = request.get_json()
        if data["roll"] == "student":
            student = Student.query.filter_by(roll_no=data["roll_no"]).first()
            if student:
                format_data = {
                    "student_id": student.student_id,
                    "name": student.name,
                    "roll_no": student.roll_no,
                    "father_name": student.father_name
                }
                if check_password_hash(data["token"], json.dumps(format_data)):
                    return jsonify({
                        "status": 200,
                        "message": "Allowed Student",
                        "bool_val": True
                    })
                return jsonify({
                    "status": 401,
                    "message": "Unauthorized Access",
                    "bool_val": False
                })
            # return student.name
        return ""