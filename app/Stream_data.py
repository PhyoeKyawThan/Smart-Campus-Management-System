from . import socket
from flask_socketio import emit
from flask import request
from .viewModel import ViewModel

@socket.on("connect")
def connected():
    view = ViewModel()
    from datetime import datetime
    passes  =view.get_passes_by_date(datetime.now().date())
    emit("pass_data", {
        "data": passes
    })
