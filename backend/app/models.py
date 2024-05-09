from . import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self) -> str:
        return self.username

class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(10), nullable=False)
    current_semester = db.Column(db.Integer, nullable=False)
    nrc = db.Column(db.String(100), nullable=False)
    father = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(200), nullable=True)

    def __init__(self,
                  name: str,
                  picture_uri: str,
                  roll_no: str,
                  current_semester: str,
                  nrc: str,
                  father: str,
                  address: str,
                  phone_no: str,
                  email: str
                    ) -> None:
        self.name = name
        self.picture_uri = picture_uri
        self.roll_no = roll_no
        self.current_semester = current_semester
        self.nrc = nrc
        self.father = father
        self.address = address
        self.phone_no = phone_no
        self.email = email        

    def __str__(self) -> str:
        return f"name - {self.name}, roll_no - {self.roll_no}"