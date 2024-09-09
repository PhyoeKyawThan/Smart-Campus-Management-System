from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_qrcode import QRcode
from flask_socketio import SocketIO
# create db object
db = SQLAlchemy()
socket = SocketIO()


def app():
    
    app = Flask(__name__)
    # integrate config file
    app.config.from_pyfile("assets/config.py")
    # initial db with app
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth
    from .student_actions import student
    from .teacher_actions import teacher
    from .staff_actions import staff
    from .guest_actions import guest
    from .file_upload import file
    from .errors import errors
    # from .stream import stream as stream_blueprint
    from .esp.controller import controller
    from . import Stream_data
    # register_blueprint
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(errors)
    app.register_blueprint(auth, url_prefix="/auth/admin")
    app.register_blueprint(student, url_prefix="/student")
    app.register_blueprint(teacher, url_prefix="/teacher")
    app.register_blueprint(staff, url_prefix="/staff")
    app.register_blueprint(guest, url_prefix="/guest")
    app.register_blueprint(file, url_prefix="/file")
    app.register_blueprint(controller, url_prefix="/controller")
    # app.register_blueprint(stream_blueprint, url_prefix="/stream")

    # database create after app 
    with app.app_context():
        db.create_all()
    # initial the socket with app
    socket.init_app(app)
    return app

app = app()
migrate = Migrate(app, db)
# initial mail object for using in all blueprint
MAIL = Mail(app=app)
qrcode = QRcode(app=app)