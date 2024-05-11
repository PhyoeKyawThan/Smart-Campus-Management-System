from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create db object
db = SQLAlchemy()

def app():
    
    app = Flask(__name__)
    # integrate config file
    app.config.from_pyfile("config.py")
    # initial db with app
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth
    from .student_register import register
    # register_blueprint
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/admin")
    app.register_blueprint(register, url_prefix="/student")
    

    # database create after app 
    with app.app_context():
        db.create_all()
    
    return app

app = app()
migrate = Migrate(app, db)