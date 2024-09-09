from . import socket
from flask_socketio import emit
from flask import request
from .viewModel import ViewModel

@socket.on("connect")
def connected():
    view = ViewModel()
    passes  =view.get_passes_by_date()
    emit("pass_data", {
        "data": passes
    })
