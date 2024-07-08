from flask import Blueprint, request, jsonify, abort
from ..assets.validate import is_admin_in_session
from .track import Track
import requests
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
    # if not is_admin_in_session():
    #     abort(401)
    if request.method == "POST":
        data = json.loads(request.args.get("data"))
        if data["id"]:
            new_track = Track(data["who"])
            if new_track.add_pass(datas=data):
                # open = requests.get("http://192.168.1.20/move?state=open");
                return jsonify({
                    "status": True,
                    "message": "Access Granted"
                })
            return jsonify({
                "status": False,
                "message": "Access Denied"
            })
        return jsonify({
            "status": "fail",
            "message": "Seem like you are using unsupported format of data"
        })
    return f"passed - {data["id"]}" 