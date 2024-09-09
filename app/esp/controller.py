from flask import Blueprint, request, jsonify, abort
from flask_socketio import emit
from ..assets.validate import is_admin_in_session
from .track import Track
from ..viewModel import ViewModel
import json

controller = Blueprint("controller", __name__)

@controller.route("/who_pass", methods=["POST", "GET"])
def who_pass():
    """
    Endpoint to handle access based on data.
    """
    # if not is_admin_in_session():
    #     abort(401)

    if request.method == "POST":
        try:
            data = json.loads(request.args.get("data"))  # Consider using request.json if passing JSON in body
        except (TypeError, ValueError):
            return jsonify({
                "status": "fail",
                "message": "Invalid data format"
            })

        if "id" in data:
            new_track = Track(data["who"])
            if new_track.add_pass(datas=data):
                # open = requests.get("http://192.168.1.20/move?state=open");
                view = ViewModel()
                passes = view.get_passes_by_date()
                
                # Emit the data
                emit("pass_data", {
                    "data": passes
                }, broadcast=True,  namespace="/")

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
            "message": "Invalid ID in the data"
        })
    return jsonify({
        "message": "GET request not supported for this endpoint"
    })
