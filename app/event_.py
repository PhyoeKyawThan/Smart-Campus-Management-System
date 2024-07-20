import time
import json
from .viewModel import ViewModel
from flask import current_app

def generate(app, who):
    view = ViewModel()
    with app.app_context():  # Ensure the application context is active
        while True:
            try:
                passes = view.gate_passes(who)
                print(passes)
                time.sleep(3)
                yield f"data: {json.dumps(passes)}\n\n"
            except Exception as e:
                current_app.logger.error(e)
                break
